import cv2
import numpy as np
drawing=False # true if mouse is pressed
mode=True
flag=0

# mouse callback function
def paint_draw(event,former_x,former_y,flags,param):
    global current_former_x,current_former_y,drawing, mode

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        current_former_x,current_former_y=former_x,former_y

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if mode==True:
                cv2.line(image,(current_former_x,current_former_y),(former_x,former_y),(255,255,255),25)
                current_former_x = former_x
                current_former_y = former_y
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode==True:
            cv2.line(image,(current_former_x,current_former_y),(former_x,former_y),(255,255,255),25)
            current_former_x = former_x
            current_former_y = former_y
    return former_x,former_y


image = cv2.imread("screen.jpg")
cv2.namedWindow("OpenCV Paint Brush")
cv2.setMouseCallback('OpenCV Paint Brush',paint_draw)
while(1):
    cv2.imshow('OpenCV Paint Brush',image)
    k=cv2.waitKey(1)& 0xFF
    if k==27: #Escape KEY
        cv2.imwrite("painted_image.jpg",image)
        flag=1
        break
cv2.destroyAllWindows()
if flag==1:
    from tensorflow.keras import models
    img=cv2.imread('painted_image.jpg')
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    resize=cv2.resize(img,(28,28),interpolation=cv2.INTER_AREA)
    resize=resize/255
    resizetest=np.array(resize).reshape(-1,28,28,1)
    model =models.load_model('handwritingmodel')
    number=np.argmax(model.predict(resizetest))


    import pygame
    pygame.mixer.init()
    pygame.init()
    done=False
    # choi1=input('pls enter the choice from (rock , paper, scissor)')
    pygame.display.set_caption('Handwriting number predictor')
    screen=pygame.display.set_mode((500,200))
    font=pygame.font.SysFont("MV Boli",30)
    text1=font.render('The recognized number is: ',True,(234,123,0))
    font2=pygame.font.SysFont("MV Boli",70)
    text2=font2.render(str(number),True,(255,255,0))
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
        screen.fill((230,200,255))
        screen.blit(text1,(50,10))
        screen.blit(text2,(200,70))
        pygame.display.flip()
    pygame.quit()
