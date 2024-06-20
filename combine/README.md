합치기 위한 코드들
폴더의 구조:

*OSS_DUdoexy
            *safety data
            *safety map   
                        * __pycache__
                        * database
                        *main
                        * manager
                        *safetymap
                        *scream_detection  
                                    *main.py
                                    *nn.py
                                    *predict.py
                        *speech_recognition
                        *static
                        *templates
                        *manage.py
이런 식으로 있어야한다.     

여기서 고친 파일들: safetymap의 main폴더의 view.py, url.py

                   scream_detection의 nn.py, test1.py(main.py), predict.py
                   
                   speech_recognition의 음성인식.py(main.py)
