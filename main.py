from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from plyer import accelerometer
import random

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stones = []
        self.tilt_x, self.tilt_y = 0, 0
        
        try:
            accelerometer.enable()
        except:
            pass # если на ПК - сенсора нет
            
        # Создаем камни
        for _ in range(6):
            self.stones.append({
                'x': Window.width / 2 + random.uniform(-100, 100),
                'y': Window.height / 2 + random.uniform(-100, 100),
                'vx': 0, 'vy': 0, 'size': 30
            })
        
        Clock.schedule_interval(self.update, 1/60.0)

    def update(self, dt):
        # Получаем данные акселерометра (наклон телефона)
        try:
            accel = accelerometer.acceleration
            if accel[0] is not None:
                self.tilt_x = accel[0] * 20
                self.tilt_y = -accel[1] * 20
        except:
            pass

        # Обновляем физику камней
        for s in self.stones:
            s['vx'] += self.tilt_x * dt
            s['vy'] += self.tilt_y * dt
            s['x'] += s['vx'] * dt
            s['y'] += s['vy'] * dt
            
            # Трение
            s['vx'] *= 0.98
            s['vy'] *= 0.98

            # Границы доски (если вылетел - возвращаем в центр)
            if s['x'] < 50 or s['x'] > Window.width - 50 or s['y'] < 50 or s['y'] > Window.height - 50:
                s['x'], s['y'] = Window.width / 2, Window.height / 2
                s['vx'], s['vy'] = 0, 0
        
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Фон (доска)
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=(0, 0), size=Window.size)
            
            # Источник света в центре (желтоватый круг с прозрачностью)
            Color(1, 0.9, 0.5, 0.2)
            Ellipse(pos=(Window.width/2 - 200, Window.height/2 - 200), size=(400, 400))
            Color(1, 0.9, 0.5, 0.4)
            Ellipse(pos=(Window.width/2 - 100, Window.height/2 - 100), size=(200, 200))

            # Камни
            Color(0.6, 0.6, 0.6, 1)
            for s in self.stones:
                Ellipse(pos=(s['x'], s['y']), size=(s['size'], s['size']))

class StonesApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    StonesApp().run()
