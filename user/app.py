import streamlit as st
from evaluate_final import run_check, run_check_video
import firebase_admin
from firebase_admin import firestore, storage
from datetime import datetime
import cv2
import tempfile


def add_to_report(score, pos, image):

    now = datetime.now()
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app()
    db = firestore.client()
    doc_ref = db.collection("users").document(st.session_state.user_id)
    report_ref = doc_ref.collection("scores").document(pos)

    # s = f"{str(pos).replace(' ', '_')}_states"
    old_data = doc_ref.get().to_dict()[f"{str(pos).replace(' ', '_')}_states"]
    if old_data["max"] == None:
        new_data = {
        "avg": score,
        "max":  score ,
        "min":  score ,
        "last": score,
        "count": 1
    }
    else:
        new_data = {
            "avg": (old_data["avg"] * old_data["count"] + score) / (old_data["count"] + 1) if old_data["avg"] > 0 else score,
            "max": max(old_data["max"], score ),
            "min": min(old_data["min"], score ),
            "last": score,
            "count": old_data["count"] + 1
        }
  

    # Adding  the IMAGES to storage
    try:
        bucket = storage.bucket("forms-data-e0050.appspot.com")
        blob = bucket.blob(f'UsersData/EvaluatedImages/{st.session_state.user_id}{pos}{new_data["count"]}.png')
        blob.upload_from_string(image, content_type='image/png')
        blob.make_public()
        # url = blob.public_url
        report_ref.set({
        str(now):
        {
        "Scroe": score,
        "image": blob.public_url
        }
        }, merge=True)
        doc_ref.update({f"{pos.replace(' ', '_')}_states": new_data})
    except Exception as e:
        st.error(f"Error occurred while submiting your score, please try again!")
    else:
        st.success(f"score added to {pos} report")

def reset_session():
    st.session_state.uploader_key += 1
    st.session_state['processed_video_path'] = None
    st.session_state['done_video_path'] = ''
    st.session_state['best_frame'] = None
    st.session_state['best_frame'] = {
    "score" : -1, 
    "frame" : [],
    "feed_back" : []
}

data = st.session_state.user
name = data['name']
st.header(f'welcome back {name}')
poses = ["front balance / ميزان امامى", "side balance / ميزان جانبى",
        "star jump / وثبة النجمة", "scissors leap / وثبة المقص",
        "pivot arabesque / دوران أرابيسك", "pivot passé / دوران بالارتكاز (باسيه)"]
pos = st.selectbox("evaluation for ...", poses, index=None, placeholder="Select pose ...", on_change=reset_session )

if pos != None : 
    pos = pos.split('/')[0].strip() # get the name of the pose

if 'processed_video_path' not in st.session_state:
    st.session_state['processed_video_path'] = None

if 'done_video_path' not in st.session_state:
    st.session_state['done_video_path'] = ''

if 'best_frame' not in st.session_state:
    st.session_state['best_frame'] = None

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

if pos in ["star jump", "scissors leap", "pivot arabesque", "pivot passé"]:
    video = st.file_uploader("Upload your video...", type=["mp4", "mov", "avi", "webm"], key=f"video_uploader_{st.session_state.uploader_key}")
    
    if video :
        if st.session_state['processed_video_path'] != video:
            st.session_state['processed_video_path'] = video
            # Save uploaded video to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(video.read())
                video_path = tmp.name

            # Open video with OpenCV
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Create temporary output video (WebM / VP8 codec)
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".webm").name
            fourcc = cv2.VideoWriter_fourcc(*"VP80")  # VP8 codec for web-friendly video
            out = cv2.VideoWriter(output_path, fourcc, 15, (width, height))
            st.session_state['done_video_path'] = output_path
            progress = st.progress(0)
            i = 0
            st.session_state['best_frame'] = {
                "score" : -1, 
                "frame" : [],
                "feed_back" : []
            }
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert BGR -> RGB for your processing function
                frame_rgb = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
                
                # Process the frame (your function)
                out_img, curr_frame_score , curr_frame_feedback = run_check_video(frame_rgb, pos)
                if curr_frame_score > st.session_state['best_frame']["score"]:
                    st.session_state['best_frame']["feed_back"] = curr_frame_feedback
                    st.session_state['best_frame']["score"] = curr_frame_score
                    st.session_state['best_frame']["frame"] = out_img
                
                # Convert processed frame back to BGR for VideoWriter
                out.write(out_img)

                i += 1
                progress.progress(i / total)

            cap.release()
            out.release()

            st.success("Pose evaluation completed!")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Analysed Video: ")
            with open(st.session_state['done_video_path'], "rb") as f:
                video_bytes = f.read()
                st.video(video_bytes)
                

        with col2:
            
            # Download button
            if st.session_state['best_frame']["score"] > -1 : 
                score = st.session_state['best_frame']["score"]
                st.header(f"You scored {score}/5")
                test = st.image(st.session_state['best_frame']["frame"], channels='BGR')

        if len(st.session_state['best_frame']["feed_back"]) > 0:
            st.markdown(
            "<div dir='rtl' style='text-align:right; color:red'>" 
            + "".join([f"<h4>{line}</h4>" for line in st.session_state['best_frame']["feed_back"]])
            + "</div>",
            unsafe_allow_html=True
        )
        is_success, buffer = cv2.imencode(".png", st.session_state['best_frame']["frame"])
        io_buf = buffer.tobytes()
        st.button("Submit Score", type="primary", use_container_width=True, on_click=add_to_report, args=(score, pos, io_buf))

       
        
                         
elif pos in ["front balance", "side balance"]:
    image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if image is not None and pos != None:
        
        l = run_check(image, pos)
        if l:
            out_img, score, feedback = l
            test = st.image(out_img, channels='BGR')
            st.title(f"You scored {score}/5")
            if len(feedback) > 0:
                st.markdown(
                "<div dir='rtl' style='text-align:right; color:red'>" 
                + "".join([f"<h4>{line}</h4>" for line in feedback])
                + "</div>",
                unsafe_allow_html=True
            )
            is_success, buffer = cv2.imencode(".png", out_img)
            io_buf = buffer.tobytes()
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Go to References", use_container_width=True):
                    st.switch_page("user/reference.py")

            with col2:
                # Create a download button
                st.download_button(
                    label="Download Image",
                    data=io_buf,
                    file_name="image.png",
                    mime="image/png",
                    use_container_width=True
                )
            st.button("Submit Score", type="primary", use_container_width=True, on_click=add_to_report, args=(score, pos, io_buf))
        else:
            st.error('invalid image, please upload another image!', icon="🚨")






