import pandas as pd
import graph


class byArea:
    df = pd.read_csv('https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_area_type_hosp_dynamics.csv')

    @classmethod
    def areaData(cls, area, df=df):
        return df[df['registration_area'] == area]

    @classmethod
    def casesByGender(cls, area):
        df = cls.areaData(area)
        res = {
            'Чоловіча': 0,
            'Жіноча': 0,
        }
        genderList = df['person_gender'].tolist()
        caseList = df['new_confirm'].tolist()
        for i in range(len(genderList)):
            if genderList[i] == 'Чоловіча':
                res['Чоловіча'] += caseList[i]
            else:
                res['Жіноча'] += caseList[i]
        return res

    @classmethod
    def allCases(cls, area):
        res = cls.casesByGender(area)
        return res['Чоловіча'] + res['Жіноча']

    @classmethod
    def allRecoveries(cls, area):
        df = cls.areaData(area)
        return sum(df['new_recover'])

    @classmethod
    def allDeaths(cls, area):
        df = cls.areaData(area)
        return sum(df['new_death'])

    @classmethod
    def casesByAge(cls, area):
        df = cls.areaData(area)
        res = {
            '0-9': 0,
            '10-19': 0,
            '20-29': 0,
            '30-39': 0,
            '40-49': 0,
            '50-59': 0,
            '60-69': 0,
            '70-79': 0,
            '80-89': 0,
            '90+': 0,
        }
        ageList = df['person_age_group'].tolist()
        caseList = df['new_confirm'].tolist()
        for i in range(len(ageList)):
            if ageList[i] == '0-9':
                res['0-9'] += caseList[i]
            elif ageList[i] == '10-19':
                res['10-19'] += caseList[i]
            elif ageList[i] == '20-29':
                res['20-29'] += caseList[i]
            elif ageList[i] == '30-39':
                res['30-39'] += caseList[i]
            elif ageList[i] == '40-49':
                res['40-49'] += caseList[i]
            elif ageList[i] == '50-59':
                res['50-59'] += caseList[i]
            elif ageList[i] == '60-69':
                res['60-69'] += caseList[i]
            elif ageList[i] == '70-79':
                res['70-79'] += caseList[i]
            elif ageList[i] == '80-89':
                res['80-89'] += caseList[i]
            else:
                res['90+'] += caseList[i]
        return res

    @classmethod
    def deathsByAge(cls, area):
        df = cls.areaData(area)
        res = {
            '0-9': 0,
            '10-19': 0,
            '20-29': 0,
            '30-39': 0,
            '40-49': 0,
            '50-59': 0,
            '60-69': 0,
            '70-79': 0,
            '80-89': 0,
            '90+': 0,
        }
        ageList = df['person_age_group'].tolist()
        deathList = df['new_death'].tolist()
        for i in range(len(ageList)):
            if ageList[i] == '0-9':
                res['0-9'] += deathList[i]
            elif ageList[i] == '10-19':
                res['10-19'] += deathList[i]
            elif ageList[i] == '20-29':
                res['20-29'] += deathList[i]
            elif ageList[i] == '30-39':
                res['30-39'] += deathList[i]
            elif ageList[i] == '40-49':
                res['40-49'] += deathList[i]
            elif ageList[i] == '50-59':
                res['50-59'] += deathList[i]
            elif ageList[i] == '60-69':
                res['60-69'] += deathList[i]
            elif ageList[i] == '70-79':
                res['70-79'] += deathList[i]
            elif ageList[i] == '80-89':
                res['80-89'] += deathList[i]
            else:
                res['90+'] += deathList[i]
        return res

    @classmethod
    def deathsByGender(cls, area):
        df = cls.areaData(area)
        res = {
            'Чоловіча': 0,
            'Жіноча': 0,
        }
        genderList = df['person_gender'].tolist()
        deathList = df['new_death'].tolist()
        for i in range(len(genderList)):
            if genderList[i] == 'Чоловіча':
                res['Чоловіча'] += deathList[i]
            else:
                res['Жіноча'] += deathList[i]
        return res

    @classmethod
    def recoveriesByAge(cls, area):
        df = cls.areaData(area)
        res = {
            '0-9': 0,
            '10-19': 0,
            '20-29': 0,
            '30-39': 0,
            '40-49': 0,
            '50-59': 0,
            '60-69': 0,
            '70-79': 0,
            '80-89': 0,
            '90+': 0,
        }
        ageList = df['person_age_group'].tolist()
        recoveryList = df['new_recover'].tolist()
        for i in range(len(ageList)):
            if ageList[i] == '0-9':
                res['0-9'] += recoveryList[i]
            elif ageList[i] == '10-19':
                res['10-19'] += recoveryList[i]
            elif ageList[i] == '20-29':
                res['20-29'] += recoveryList[i]
            elif ageList[i] == '30-39':
                res['30-39'] += recoveryList[i]
            elif ageList[i] == '40-49':
                res['40-49'] += recoveryList[i]
            elif ageList[i] == '50-59':
                res['50-59'] += recoveryList[i]
            elif ageList[i] == '60-69':
                res['60-69'] += recoveryList[i]
            elif ageList[i] == '70-79':
                res['70-79'] += recoveryList[i]
            elif ageList[i] == '80-89':
                res['80-89'] += recoveryList[i]
            else:
                res['90+'] += recoveryList[i]
        return res

    @classmethod
    def recoveriesByGender(cls, area):
        df = cls.areaData(area)
        res = {
            'Чоловіча': 0,
            'Жіноча': 0,
        }
        genderList = df['person_gender'].tolist()
        recoveryList = df['new_recover'].tolist()
        for i in range(len(genderList)):
            if genderList[i] == 'Чоловіча':
                res['Чоловіча'] += recoveryList[i]
            else:
                res['Жіноча'] += recoveryList[i]
        return res

    @classmethod
    def dataByDate(cls, area, date):
        df = cls.areaData(area)
        df = df[df['zvit_date'] == date]
        df = df[['new_susp', 'new_confirm', 'active_confirm', 'new_death', 'new_recover']]
        df = df.sum(axis=0)
        new_susp = df['new_susp']
        new_confirm = df['new_confirm']
        active_confirm = df['active_confirm']
        new_death = df['new_death']
        new_recover = df['new_recover']
        res = {
            'Нові підозри': new_susp,
            'Нові підтверджені випадки': new_confirm,
            'Кількість хворих': active_confirm,
            'Смертність': new_death,
            'Кількість одужавших': new_recover
        }
        return res

    @classmethod
    def curIllnesses(cls, area, df=df):
        dateList = df['zvit_date'].tolist()
        date = dateList[0]
        resList = cls.dataByDate(area, date)
        return resList['Кількість хворих']

    @classmethod
    def dynamics(cls, area, *args):
        df = cls.areaData(area)
        graph.draw(df, area, *args)

    cityList = df['registration_area'].tolist()
    areaList = []
    for i in cityList:
        if i not in areaList:
            areaList.append(i)

    @classmethod
    def areasComparison(cls, arg, areaList=areaList):
        res = {}
        if arg != 'active_confirm':
            for area in areaList:
                tempDf = cls.areaData(area)
                res[area] = sum(tempDf[arg])
        else:
            for area in areaList:
                temp = cls.curIllnesses(area)
                res[area] = temp
        return res

    @classmethod
    def toExcel(cls, path, df=df):
        dateList = df['zvit_date'].tolist()
        lastDate = dateList[0]
        df = df[df['zvit_date'] == lastDate]
        df = df[['registration_area', 'new_susp', 'new_confirm', 'active_confirm', 'new_death', 'new_recover']]
        df = df.groupby(['registration_area']).agg('sum')
        try:
            df.to_excel(path)
        except Exception as e:
            print(e)
        else:
            print('Done!')

    @classmethod
    def userMenu(cls, areaList=areaList, df=df):
        allCases = 0
        for i in areaList:
            allCases += cls.allCases(i)
        allDeaths = 0
        for i in areaList:
            allDeaths += cls.allDeaths(i)
        allRecoveries = 0
        for i in areaList:
            allRecoveries += cls.allRecoveries(i)
        print(f'Всі випадки у Україні: {allCases}\n'
              f'Серед них:\n'
              f'\tОдужали: {allRecoveries}\n'
              f'\tПомерли: {allDeaths}\n')
        while True:
            print('Оберіть регіон для детальної інформації:')
            for i in range(len(areaList)):
                print(f"{i+1}) {areaList[i]}")
            print('Вивести дані на карту - map')
            print('Завантажити дані за останній день в таблицю excel - table')
            print('Вийти - exit')
            num = input()
            if num == 'exit':
                exit()
            if num == 'map':
                args = ['new_susp', 'new_confirm', 'active_confirm', 'new_death', 'new_recover']
                print(f"Введіть номер поля для відображення:\n"
                      f"\t1) Підозри\n"
                      f"\t2) Підтверджені випадки\n"
                      f"\t3) Хворі\n"
                      f"\t4) Смертність\n"
                      f"\t5) Одужавші")
                num = int(input())
                arg = args[num-1]
                graph.onMap(cls.areasComparison(arg), arg)
                cls.userMenu()
            if num == 'table':
                print('Enter path where table will be saved to:')
                path = input()
                cls.toExcel(path)
                cls.userMenu()
            area = areaList[int(num)-1]
            strArea = area
            if area != 'м. Київ':
                strArea += ' область'
            print(f'Всі випадки в регіоні {strArea}: {cls.allCases(area)}\n'
                  f'Серед них:\n'
                  f'\tОдужали: {cls.allRecoveries(area)}\n'
                  f'\tПомерли: {cls.allDeaths(area)}\n')
            while True:
                print(f'Оберіть наступний крок:\n'
                      f'1) Згрупувати за віком\n'
                      f'2) Згрупувати за статтю\n'
                      f'3) Дані за певну дату\n'
                      f'4) Динаміка\n'
                      f'5) Повернутися до вибору регіону\n'
                      f'Вийти - exit')
                num = input()
                if num == 'exit':
                    exit()
                num = int(num)
                if num == 1:
                    cases = cls.casesByAge(area)
                    recoveries = cls.recoveriesByAge(area)
                    deaths = cls.deathsByAge(area)
                    for i in cases:
                        print(f"{i}:\n"
                              f"\tВипадки: {cases[i]}\n"
                              f"\tОдужали: {recoveries[i]}\n"
                              f"\tПомерли: {deaths[i]}")
                    print('\n')
                if num == 2:
                    cases = cls.casesByGender(area)
                    recoveries = cls.recoveriesByGender(area)
                    deaths = cls.deathsByGender(area)
                    for i in cases:
                        print(f"{i}:\n"
                              f"\tВипадки: {cases[i]}\n"
                              f"\tОдужали: {recoveries[i]}\n"
                              f"\tПомерли: {deaths[i]}")
                    print('\n')
                if num == 3:
                    print('Введіть дату у форматі YYYY-MM-DD')
                    date = input()
                    byDate = cls.dataByDate(area, date)
                    for i in byDate:
                        print(f"\t{i}: {byDate[i]}")
                    print('\n')
                if num == 4:
                    args = ['new_susp', 'new_confirm', 'active_confirm', 'new_death', 'new_recover']
                    print(f"Введіть через пробіл номери полів для відображення:\n"
                          f"\t1) Підозри\n"
                          f"\t2) Підтверджені випадки\n"
                          f"\t3) Хворі\n"
                          f"\t4) Смертність\n"
                          f"\t5) Одужавші")
                    numsOfArgs = input().split(' ')
                    for i in range(len(numsOfArgs)):
                        numsOfArgs[i] = int(numsOfArgs[i])
                    activeArgs = []
                    for i in numsOfArgs:
                        activeArgs.append(args[i-1])
                    cls.dynamics(area, activeArgs)
                if num == 5:
                    break
