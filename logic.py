import gradio as gr
import random
import json

def get_by_level(level): 
    with open('./settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
    return settings[level]   
def set_target(choice,target_problems,prombelms_state,settings_state,score_board_visible_state):# 设置target :#state1 是 问题个数 #state2是问题设置 #state3是设置记分牌的可见性
    settings_state = get_by_level(choice)   
    return settings_state,target_problems,gr.update(visible=False),True     
def check_range(result,settings):
    return result >=settings["answer_range"][0] and result <=settings["answer_range"][1]
def sub(lst):
    if not lst:  # 检查列表是否为空
        return 0  # 或者抛出异常，根据你的需求
    result = lst[0]  # 初始值为列表的第一个元素
    for num in lst[1:]:  # 从第二个元素开始遍历
        result -= num 
    return result

# 尝试分开键盘render 失败！ 

def create_problem_impl(settings):

    nums = random.choice([i for i in range(settings["number_nums"][0],settings["number_nums"][1]+1)])
    
    nums_waitbechoice=[i for i in range(settings["number_range"][0],settings["number_range"][1]+1)]
    
    problem_nums = [random.choice(nums_waitbechoice) for i in range(nums)]
   
    way = random.choice(settings["way"])
    
    if way =="+":
        counter = 0 # 计算失败次数
        result = sum(problem_nums)
        while not check_range(result,settings):
            counter += 1
            if counter > 1000:
                return create_problem_impl(settings)
            random.shuffle(problem_nums)
            result = sum(problem_nums)
            

        return problem_nums,result,["+" for i in range(nums-1)]
    if way =="-":
        counter = 0 # 计算失败次数
        result = sub(problem_nums)
        while not check_range(result,settings):
            counter += 1
            if counter > 1000:
                return create_problem_impl(settings)
            random.shuffle(problem_nums)
            result = sub(problem_nums)

        return problem_nums,result,["-" for i in range(nums-1)]
    if way =="+-":

        counter = 0 # 计算失败次数
        signal_list = []
        while True:
            result = problem_nums[0]
            signal_list= []
            for i in range(1,nums):
                choice = random.choice(["+","-"])
                if choice == "+":
                    result += problem_nums[i]
                    signal_list.append("+")
                else:
                    result -= problem_nums[i]
                    signal_list.append("-")
                if result < 0:
                    break 
            if check_range(result,settings):
                break
            else:
                counter += 1
                if counter > 100:
                    return create_problem_impl(settings)
                else: 
                    random.shuffle(problem_nums)
        print("nums:",nums)
        print("nums_waitbechoice:",nums_waitbechoice)
        print("problem_nums:",problem_nums)
        print("way:",way)
        return problem_nums,result,signal_list

def create_problem(settings,true_answer_state,generated_state):
    problem_num,true_answer,signal_list = create_problem_impl(settings)
    text = str(problem_num[0])
    for i in range(1,len(problem_num)):
        text += signal_list[i-1] + str(problem_num[i])
    print(text,true_answer)
    return text,true_answer,True      
def answer_problem(answer,true_answer_state,right,wrong,generated_state,history,problem_article):
    print(answer,true_answer_state)
    if answer== str(true_answer_state):
        right += 1
        print("Yes")
        return right,wrong,False,history
    else:
        wrong += 1
        print("No")
        history.append({problem_article:true_answer_state,"错误答案":answer})
        return right,wrong,False,history
    