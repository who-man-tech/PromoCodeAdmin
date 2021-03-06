import json
import os
from io import StringIO
import re

from django.test import TestCase
from django.core.management import call_command

from app.settings import BASE_DIR
from promo_code.services import generate_promo_code




class CommandsTestCase(TestCase):
    def test_cammand_gen_code(self):
        """
        Тест комманды, которая генерирует новые промо коды.
        """
        
        # Путь до тестового файла кодов
        file_path = os.path.join(BASE_DIR, "promo_code", "tests", "codes.json")
        # Удаляем файл с кодами, если он есть
        try:
            os.remove(file_path)
        except:
            pass

        # Запускаем команды
        call_command('gen_codes',**{"amount": 10,
                                    "group": "агенства",
                                    "path": file_path})
        call_command('gen_codes',**{"amount": 1,
                                    "group": "агенства",
                                    "path": file_path})
        call_command('gen_codes',**{"amount": 42,
                                    "group": "avtostop",
                                    "path": file_path})
        call_command('gen_codes',**{"amount": 5,
                                    "group": 1,
                                    "path": file_path})

        
        data = None
        with open(file_path) as file:
            data = json.load(file)
        # Находим количесво групп и кодов
        groups = []
        codes_count = 0
        for object in data["data"]:
            # Если название группы есть в списке уже найденных групп
            if object["group"] not in groups:
                # Если группы нет в списке найденных групп
                # Добавляем ее в этот список
                groups.append(object["group"])
            # Добавляем к числу кодов количество кодов этой группы
            codes_count += len(object["codes"])

        # Удаляем тестовый файл с кодами
        os.remove(file_path)

        self.assertEqual(len(groups), 3)
        self.assertEqual(codes_count, 58)



    def test_cammand_get_code(self):
        """
        Тест комманды, которая находит группу указанного кода.
        """
        
        # Путь до тестового файла кодов
        file_path = os.path.join(BASE_DIR, "promo_code", "tests", "codes.json")

        # Удаляем файл с кодами, если он есть
        try:
            os.remove(file_path)
        except:
            pass

        groups = ["агенства", "агенства", "avtostop", 1]
        codes = []
        # Создаем файл с кодами
        for g in groups:
            codes.append(generate_promo_code(amount=5, group=g, file_path=file_path)[0])

        out = StringIO()

        # Запускаем комманду, которая будет искать код файле
        for i in range(len(groups)):
            call_command('get_code_group',
                         **{"code": codes[i],
                            "path": file_path},
                         stdout=out)

            # Проверем, что каждому коду соответствует его группа
            self.assertIsNotNone(re.search(str(groups[i]), out.getvalue()))

        # Удаляем тестовый файл с кодами
        os.remove(file_path)