# desision trees for scores: 
    #   "RIGHT_KNEE",
    #   "LEFT_KNEE" 
    #   "LEFT_HIP", 
    #   "RIGHT_HIP"
    #   "LEFT_ANKLE"
    #   "angle_between_leg"
def front_balance_score(angles : dict): 
    print(angles)
    if angles["angle_between_leg"] >= 85: 
        if angles["RIGHT_KNEE"] >= 170 : 
            if angles["LEFT_KNEE"] >= 170 : 
                if angles["RIGHT_HIP"] >= 85 :
                    if angles["LEFT_HIP"] <= 185 :
                        return 10
                    else: 
                        return 9
                    
                else: 
                    if angles["LEFT_HIP"] <= 185 :
                        return 9
                    else: 
                        return 8
            
            else: 
                if angles["RIGHT_HIP"] >= 85 :
                    if angles["LEFT_HIP"] <= 185 :
                        return 9
                    else: 
                        return 8
                    
                else: 
                    if angles["LEFT_HIP"] <= 185 :
                        return 8
                    else: 
                        return 7
            
        else: 
            if angles["LEFT_KNEE"] >= 170 : 
                if angles["RIGHT_HIP"] >= 85 :
                    if angles["LEFT_HIP"] <= 185 :
                        return 9
                    else: 
                        return 8
                    
                else: 
                    if angles["LEFT_HIP"] <= 185 :
                        return 8
                    else: 
                        return 7
            
            else: 
                if angles["RIGHT_HIP"] >= 85 :
                    if angles["LEFT_HIP"] <= 185 :
                        return 8
                    else: 
                        return 7
                    
                else: 
                    if angles["LEFT_HIP"] <= 185 :
                        return 7
                    else: 
                        return 6
      
    else :
        if angles["RIGHT_KNEE"] >= 170 : 
            if angles["LEFT_KNEE"] >= 170 : 
                if angles["RIGHT_HIP"] >= 85 :
                    if angles["LEFT_HIP"] <= 185 :
                        return 8
                    else: 
                        return 7
                    
                else: 
                    if angles["LEFT_HIP"] <= 185 :
                        return 7
                    else: 
                        return 6
            
            else: 
                if angles["RIGHT_HIP"] >= 85 :
                    if angles["LEFT_HIP"] <= 185 :
                        return 7
                    else: 
                        return 6
                    
                else: 
                    if angles["LEFT_HIP"] <= 185 :
                        return 6
                    else: 
                        return 5
            
        else: 

            if angles["LEFT_KNEE"] >= 170 : 
                if angles["RIGHT_HIP"] >= 85 :
                    if angles["LEFT_HIP"] <= 185 :
                        return 7
                    else: 
                        return 6
                    
                else: 
                    if angles["LEFT_HIP"] <= 185 :
                        return 6
                    else: 
                        return 5
            
            else: 
                if angles["RIGHT_HIP"] >= 85 :
                    if angles["LEFT_HIP"] <= 185 :
                        return 6
                    else: 
                        return 5
                    
                else: 
                    if angles["LEFT_HIP"] <= 185 :
                        return 5
                    else: 
                        return 4
