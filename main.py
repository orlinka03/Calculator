import flet as ft
import pyperclip as pc

class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text

class DigitButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.GREY_800
        self.color = ft.colors.WHITE
        self.height = 50
        self.width = 70

class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.GREY_800
        self.color = ft.colors.ORANGE_700
        self.height = 50
        self.width = 70

class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE_700
        self.color = ft.colors.WHITE
        self.height = 50
        self.width = 70

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()

        self.adaptive = True
        self.theme_mode = 'dark'
        self.height = 430
        self.width = 400
        self.result = ft.Text('0', size=40)

        self.history = dict()

        self.expression = ft.Text("", color=ft.colors.GREY_400, size=20)

        self.reset()

        bs = ft.BottomSheet(
            content=ft.Container(
                padding=50,
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.Text("This is bottom sheet's content!"),
                        ft.ElevatedButton("Close bottom sheet", on_click=lambda _: self.close(bs)),
                    ],
                ),
            ),
        )

        # self.bs = ft.BottomSheet(
        #     ft.Container(
        #         ft.Column(
        #             [
        #                 ft.Text("This is sheet's content!"),
        #                 ft.ElevatedButton(
        #                     "Close bottom sheet", on_click=self.close_bs
        #                 ),
        #             ],
        #             tight=True,
        #         ),
        #         padding=10,
        #     ),
        #     open=False
        # )
        #
        # self.bs = ft.BottomSheet(
        #     ft.Container(
        #         ft.Column(
        #             [
        #                 ft.Text("Журнал пуст")
        #             ]
        #         )
        #     ), open=False
        # )

        self.content = ft.Column(
                    controls=[
                        ft.Row([ft.IconButton(ft.icons.COPY, on_click=self.copy_res,
                                    tooltip="Копировать", bgcolor=ft.colors.GREY_800),
                                ft.Container(expand=True),
                                ft.IconButton(ft.icons.HISTORY, on_click=lambda _: self.open(bs))]),
                        ft.Row([self.expression], scroll=ft.ScrollMode.AUTO),
                        ft.Row([self.result], scroll=ft.ScrollMode.AUTO),
                        ft.Row([
                            ActionButton(text="C", button_clicked=self.button_clicked),
                            ActionButton(text="⌫", button_clicked=self.button_clicked),
                            ActionButton(text="^", button_clicked=self.button_clicked),
                            ActionButton(text="/", button_clicked=self.button_clicked),
                        ], ft.MainAxisAlignment.SPACE_AROUND),

                        ft.Row([
                            DigitButton(text="7", button_clicked=self.button_clicked),
                            DigitButton(text="8", button_clicked=self.button_clicked),
                            DigitButton(text="9", button_clicked=self.button_clicked),
                            ActionButton(text="*", button_clicked=self.button_clicked),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),

                        ft.Row([
                            DigitButton(text="4", button_clicked=self.button_clicked),
                            DigitButton(text="5", button_clicked=self.button_clicked),
                            DigitButton(text="6", button_clicked=self.button_clicked),
                            ActionButton(text="-", button_clicked=self.button_clicked),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),

                        ft.Row([
                            DigitButton(text="1", button_clicked=self.button_clicked),
                            DigitButton(text="2", button_clicked=self.button_clicked),
                            DigitButton(text="3", button_clicked=self.button_clicked),
                            ActionButton(text="+", button_clicked=self.button_clicked),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),

                        ft.Row([
                            ActionButton(text="%", button_clicked=self.button_clicked),
                            DigitButton(text="0", button_clicked=self.button_clicked),
                            ActionButton(text=".", button_clicked=self.button_clicked),
                            ExtraActionButton(text="=", button_clicked=self.button_clicked),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ]
        )

    # async def show_bs(self, e):
    #     self.bs.open = True
    #     await self.bs.update_async()
    #
    # async def close_bs(self, e):
    #     self.bs.open = False
    #     await self.bs.update_async()
    #
    # # happens when example is added to the page (when user chooses the BottomSheet control from the grid)
    # def did_mount(self):
    #     self.page.overlay.append(self.bs)
    #     self.page.update()
    #
    # # happens when example is removed from the page (when user chooses different control group on the navigation rail)
    # def will_unmount(self):
    #     self.page.overlay.remove(self.bs)
    #     self.page.update()

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")

        if data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
            if(self.result.value == "Глупыш какой" or
                    type(self.result.value) != str):
                self.result.value = data
                self.new_operand = False
                if self.operator is None:
                    self.expression.value = ""
            elif (self.result.value == "0" or self.new_operand == True):
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value += data

        elif data in("."):
            if self.result.value == "0":
                self.result.value = "0" + data
            elif type(self.result.value) is not str:
                self.result.value = "0" + data
                self.expression.value = ""
            elif "." in self.result.value:
                return
            else:
                self.result.value += data

        elif data in ("-"):
            if self.operator is None:
                self.operator = data
                self.operand1 = float(self.result.value)
                self.new_operand = True
                self.expression.value = f"{self.formater(self.operand1)} {self.operator}"
                print(f"{self.formater(self.operand1)} {self.operator}")
            elif self.new_operand == False and self.operand1 is None:
                self.result.value = "-"
            elif self.new_operand == True and self.operand2 is None:
                self.result.value = "-"
                self.new_operand = False
            elif self.operand1 is not None and self.operator is not None:
                if type(self.result.value) is str:
                    self.result.value = self.calculate(self.operand1,
                                                       self.formater(float(self.result.value)), self.operator)
                    self.operand1 = float(self.result.value)
                    self.operator = data
                    self.expression.value = f"{self.formater(self.operand1)} {self.operator}"
                else:
                    self.result.value = "-"

        elif data in ("+", "*", "/", "^"):
            if self.operand1 is not None and self.operator is not None:
                self.result.value = self.calculate(self.operand1,
                                                   self.formater(float(self.result.value)), self.operator)
                self.operand1 = float(self.result.value)
                self.operator = data
                self.expression.value = f"{self.formater(self.operand1)} {self.operator}"
            else:
                self.operator = data
                self.operand1 = float(self.result.value)
                self.expression.value = f"{self.formater(self.operand1)} {self.operator}"
                print(f"{self.formater(self.operand1)} {self.operator}")
                self.new_operand = True

        elif data in("%"):
            self.result.value = self.formater(float(self.result.value) * 0.01)

        elif data in ("="):
            if self.operand1 == None:
                return
            self.operand2 = float(self.result.value)
            self.expression.value = f"{self.formater(self.operand1)} {self.operator} {self.formater(self.operand2)} ="
            print(self.expression)
            self.result.value = self.calculate(self.operand1, self.operand2, self.operator)
            self.reset()

        elif data in ("C"):
            self.result.value = "0"
            self.new_operand = False
            self.expression.value = ""
            self.reset()

        elif data in "⌫":
            self.result.value = str(self.formater(float(self.result.value) // 10))

        self.update()

    def reset(self):
        self.operand1 = None
        self.operand2 = None
        self.operator = None

    def calculate(self, operand1, operand2, operator):
        a = 0
        if operator == "+":
            a = self.formater(operand1 + operand2)
            self.history[f"{self.formater(operand1)} {operator} {self.formater(operand2)} ="] = a
            print(self.history)
            return a

        if operator == "-":
            a = self.formater(operand1 - operand2)
            self.history[f"{self.formater(operand1)} {operator} {self.formater(operand2)} ="] = a
            print(self.history)
            return a

        if operator == "*":
            a = self.formater(operand1 * operand2)
            self.history[f"{self.formater(operand1)} {operator} {self.formater(operand2)} ="] = a
            print(self.history)
            return a

        if operator == "/":
            if operand2 == 0:
                return "Глупыш какой"
            else:
                a = self.formater(operand1 / operand2)
                self.history[f"{self.formater(operand1)} {operator} {self.formater(operand2)} ="] = a
                print(self.history)
                return a

        if operator == "^":
            if (self.operand1 == 0 and self.operand2 == 0) or self.operand1 == 0 and self.operand2 < 0:
                return "Глупыш какой"
            else:
                a = self.formater(operand1 ** operand2)
                self.history[f"{self.formater(operand1)} {operator} {self.formater(operand2)} ="] = a
                print(self.history)
                return a
        self.reset()

    def formater(self, num):
        if num%1 == 0:
            return int(num)
        else:
            return num

    def copy_res(self, e):
        pc.copy(self.result.value)
        print("copy_clicked")

def main(page: ft.Page):
    page.window.width = 430
    page.window.height = 510
    page.window.max_width = 430
    page.window.max_height = 510
    page.window.min_width = 430
    page.window.min_height = 510
    page.title = "Калькулятор"
    calc = CalculatorApp()
    page.add(calc)

ft.app(target=main)