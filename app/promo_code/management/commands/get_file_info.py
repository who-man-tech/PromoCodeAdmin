from django.core.management.base import BaseCommand

from promo_code.services import get_code_file_info
from promo_code.apps import PromoCodeConfig


class Command(BaseCommand):
    help = "Выводит количество групп и кодов в файле."

    def add_arguments(self, parser):
        parser.add_argument("-p",
                            "--path",
                            type=str,
                            default=PromoCodeConfig.promo_codes_file_path,
                            help="Путь к файлу с кодами")


    def handle(self, *args, **kwargs):
        path = kwargs["path"]

        if path is None or path == "" :
            self.stdout.write("Укажите путь: -p <путь к файлу>")
            return
        try:
            info = get_code_file_info(path)
        except FileNotFoundError:
            self.stdout.write("Файл не найден")
            self.stdout.write("Проверьте путь к файлу")
            return
        except ValueError:
            self.stdout.write("Не получается получить данные из файла")
            self.stdout.write("Проверьте содержимое файла")
            return
        except AssertionError:
            self.stdout.write("Неверно указаны параметры команды")
            return
        
        if info is None:            
            self.stdout.write("Не удалось получить данные о файле")
            self.stdout.write("Проверьте содержимое")
            return
        self.stdout.write(f"В файле {info['groups']} групп, {info['codes']} промо кодов")
        