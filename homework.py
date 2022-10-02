from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> None:
        t = asdict(self)
        return self.MESSAGE.format(*t.values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_COEFF_CALORIE_1: int = 18
    RUN_COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.RUN_COEFF_CALORIE_1
                * self.get_mean_speed() - self.RUN_COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * (self.duration
                * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_COEFF_CALORIE_1: float = 0.035
    WLK_COEFF_CALORIE_2: float = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.WLK_COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WLK_COEFF_CALORIE_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWM_COEFF_CALORIE_1: float = 1.1
    SWM_COEFF_CALORIE_2: int = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWM_COEFF_CALORIE_1)
                * self.SWM_COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_parameters = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in train_parameters:
        return train_parameters[workout_type](*data)
    else:
        raise ValueError("Тренировка не найдена")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)