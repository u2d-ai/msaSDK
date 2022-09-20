
class ClickDemo:
    """
    demo for click handling
    """

    async def onDivClick(self, msg):
        """
        handle a click on the Div
        """
        print(msg)
        self.clickCount += 1
        msg.target.text = f"I was clicked {self.clickCount} times"

    async def click_demo(self):
        """
        the example Webpage under test
        """
        import msaSDK.jpui as jp
        wp = jp.WebPage(debug=False)
        self.clickCount = 0
        d = jp.Div(
            text="Not clicked yet",
            a=wp,
            classes="w-48 text-xl m-2 p-1 bg-blue-500 text-white",
        )
        d.on("click", self.onDivClick)
        d.additional_properties = [
            "screenX",
            "pageY",
            "altKey",
            "which",
            "movementX",
            "button",
            "buttons",
        ]

        return wp


async def click_demo():
    clickDemo = ClickDemo()
    return await clickDemo.click_demo()
