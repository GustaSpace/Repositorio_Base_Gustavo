import pyautogui as pg
pg.mouseInfo

#pg.moveTo(100, 150, duration=1.5)
#pg.moveTo(100, 350, duration=1.5)

pg.press("win")

#espera um segundo
pg.sleep(1)
#digita chrome
pg.write("Chrome", interval= 0.5)
#entra no chrome
pg.press("enter")
#digita o saite e entra
pg.sleep(2)
pg.write("www.youtube.com")
pg.press('enter')

pg.moveTo(100,150, duration=1)

#move o mouse para a caixa de pesquisa do youtube
pg.moveTo(702,119, duration=0.5)
pg.sleep(2)
pg.click()

pg.write("travis scott", interval=0.5)
pg.press("enter")

pg.sleep(2)
pg.moveTo(597,311, duration=0.5)
pg.click

