import matplotlib as mpl
import matplotlib.pyplot as plt
import areas


def draw(df, area, args):
    resArea = area
    if area != 'м. Київ':
        resArea = area[:-1] + 'ій області'
    colors = ['red', 'green', 'blue', 'black', 'orange']
    df = df[df['registration_area'] == area]
    dateList = df['zvit_date'].tolist()
    tempList = []
    for i in dateList:
        if i not in tempList:
            tempList.append(i)
    dateList = tempList
    xticksList = []
    for i in dateList:
        if i[-2]+i[-1] == '01' or i[-2]+i[-1] == '16':
            xticksList.append(i)
        else:
            xticksList.append(' ')
    df = df[['zvit_date', 'new_susp', 'new_confirm', 'active_confirm', 'new_death', 'new_recover']]
    counter = 0
    mpl.rcParams.update({'font.size': 30})
    fig = plt.figure(dpi=30, figsize=(40, 20))
    for arg in args:
        if arg == 'new_susp':
            label = 'Підозри'
        elif arg == 'new_confirm':
            label = 'Підтверджені випадки'
        elif arg == 'active_confirm':
            label = 'Хворі'
        elif arg == 'new_death':
            label = 'Смертність'
        else:
            label = 'Одужавші'
        argList = []
        for date in dateList:
            temp_df = df[df['zvit_date'] == date]
            temp_df = temp_df.sum(axis=0)
            argList.append(temp_df[arg])
        plt.plot(dateList[::-1], argList[::-1], colors[counter], label=label, linestyle='solid', linewidth=3)
        plt.xlabel('Дата', fontsize=40)
        plt.ylabel('Кількість', fontsize=40)
        plt.title(f'Динаміка COVID-19 в {resArea}', fontsize=50)
        plt.xticks(range(len(dateList)), xticksList[::-1], fontsize=30)
        plt.grid(True)
        plt.legend(loc='upper right', fontsize=30)
        fig.autofmt_xdate(rotation=90)
        counter += 1
    plt.show()


def toType(max, cur):
    inPerCent = cur/max*100
    return 3000/100*inPerCent


def onMap(data, arg):
    if arg == 'new_susp':
        title = 'підозр на COVID-19'
    elif arg == 'new_death':
        title = 'смертей від COVID-19'
    elif arg == 'new_recover':
        title = 'одужавших від COVID-19'
    elif arg == 'new_confirm':
        title = 'усіх хворих на COVID-19 за весь час'
    else:
        title = 'хворих на COVID-19 на даний момент'
    valueList = []
    for key in data:
        valueList.append(data[key])
    maxValue = max(valueList)
    BBox = [22.427, 40.444, 44.005, 52.643]
    fig, ax = plt.subplots(figsize=[11, 8])
    img = mpl.pyplot.imread('map.png')
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    plt.title(f'Розподіл {title} в Україні')
    note = ''
    for i in areas.coordinates:
        x = areas.getLon(i)
        y = areas.getLat(i)
        type = toType(maxValue, data[i])
        ax.scatter(x, y, alpha=0.5, s=type, c='r', label=f'{i} - {data[i]}')
        note += f'{i} - {data[i]}\n'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.01, 0.01, note, transform=ax.transAxes, fontsize=6,
            verticalalignment='bottom', bbox=props)
    ax.imshow(img, extent=BBox, aspect='auto')
    plt.show()

