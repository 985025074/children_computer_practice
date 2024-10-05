import gradio as gr

from logic import *

css = """
#difficulty {
    width: 400px;
    margin: 0 auto; /* 通过 margin 自动水平居中 */
    text-align: center; /* 设置文本居中 */
}
#keylayout {
    width: 60%;
    margin: 0 auto; /* 通过 margin 自动水平居中 */
    text-align: center; /* 设置文本居中 */
}
#keys
{
    width: 100%;
    margin: 0 auto; /* 通过 margin 自动水平居中 */
    text-align: center; /* 设置文本居中 */
}
"""
import gradio as gr

with gr.Blocks(css=css) as demo:
    settings = gr.State({})
    problems = gr.State(0)
    right =gr.State(0)
    wrong = gr.State(0)
    score_board_visible =gr.State(False)
    true_answer = gr.State("")
    generated = gr.State(False)
    history = gr.State([])
    # 处理计分板的逻辑
    @gr.render(inputs=[problems,right,wrong,score_board_visible])
    def update_score(problems,right,wrong,_visbile):
        with gr.Row(visible=_visbile) as score_borad:
            gr.Markdown("## 还有{}题！,答对{},答错{},正确率{:.2f}%".format(problems-right-wrong,right,wrong,right/(right+wrong+0.000001)*100))
   # 答题完毕逻辑
    @gr.render(inputs=[right,wrong,problems,history])
    def show_result(right,wrong,problems,history):
        if right + wrong == problems and problems!= 0:
            gr.Markdown("## 答题完毕！,答对{},答错{},正确率{:.2f}%".format(right,wrong,right/(right+wrong+0.000001)*100))
            for i in history:
                gr.Markdown("{}".format(i))
   
   #预设逻辑
    with gr.Row() as target_set :
        choice = gr.Radio([("10以内","1"),("10以内,可能有4个数","2"),("50以内","3")],value = "1",info = "选择难度",scale = 4)       
        target_problems = gr.Number(label="目标题目数",value=10,scale=3)
        btn_set_target = gr.Button("设置目标",scale = 1)
        btn_set_target.click(set_target,inputs=[choice,target_problems,settings,problems,score_board_visible],outputs=[settings,problems,target_set,score_board_visible])
    @gr.render(triggers=[score_board_visible.change,generated.change,generated.change],inputs=[generated])
    def _(generated_state):
        # 基本的答题区域逻辑 
        print("generated：",generated.value)
        with gr.Row(elem_id = "work") as work_area:
            problem = gr.Textbox(label ="请解决",scale = 1,key=0)
            answer = gr.Textbox(label ="答案",scale = 1)
        
        #键盘逻辑
        if generated_state == True :
            with gr.Column(elem_id="keylayout",scale=0) as KeyBoard:
                buttons = []
                for i in range(3):
                    with gr.Row(elem_id="keys"): 
                        for j in range(3):
                            number = str(i*3+j)
                            number_btn =gr.Button(value=f"{i*3+j}",scale = 1,min_width=50)
                            buttons.append(number_btn)
                            @number_btn.click(inputs= answer,outputs= answer)
                            def input_answer(answer,key = number):
                                answer +=key
                                return answer
                btn9 = gr.Button(value="9",scale = 1)
                @btn9.click(inputs= answer,outputs= answer)
                def input_answer(answer,key = "9"):
                    answer +=key
                    return answer
        if generated_state == False:
            generate_button = gr.Button("生成")                     
            generate_button.click(create_problem,inputs=[settings,true_answer,generated],outputs=[problem,true_answer,generated]) #生成题目逻辑
        if generated_state == True:
            btn_clear = gr.Button("清空")
            @btn_clear.click(outputs = [answer])
            def clear_answer():
                return gr.update(value="")
            btn = gr.Button("回答")
            btn.click(answer_problem,inputs = [answer,true_answer,right,wrong,generated,history,problem],outputs = [right,wrong,generated,history]) #运算器逻辑
            @btn.click(outputs = [answer])#清空
            def clear_answer():
                return gr.update(value="")
            @btn.click(outputs = [problem])#清空
            def clear_problem():
                return gr.update(value="")
        # btn.click(fn = create_problem)


demo.launch(server_name="0.0.0.0", server_port=7860, share=False)