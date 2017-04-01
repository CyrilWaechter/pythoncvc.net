from Autodesk.Revit.UI import IExternalEventHandler, IExternalApplication, Result, ExternalEvent, IExternalCommand
from Autodesk.Revit.DB import Form

class ExternalEventExample(IExternalEventHandler):
    def execute(self, app):
        TaskDialog.Show("External Event", "Click Close to close")
    def GetName(self):
        return "External Event Example"


class ExternalEventExampleApp(IExternalApplication):
    def __init__(self, app = None, my_form):
        self.app = app
        self.my_form = my_form

    def on_shutdown(self, application):
        if(self.my_form is not None and self.my_form.Visible):
            self.myForm.Close()
        return Result.Succeeded

    def on_startup(self, application):
        self.my_form = None
        return Result.Succeeded

    def show_form(self, application):
        if self.my_form == None or self.my_form.Disposed:
            handler = ExternalEventExample()
            ex_event = ExternalEvent.Create(handler)

            self.my_form = ExternalEventExampleDialog(ex_event, handler)
            self.my_form.Show()

class Command(IExternalCommand):
    def execute(self, command_data, message, elements):
        try:
            ExternalEventExampleApp.show_form(command_data.Application)
            return Result.Succeeded
        except:
            raise
            return Result.Failed

class ExternalEventExampleDialog(Form):
    def __init__(self, ex_event, handler):
        self.ex_event = ex_event
        self.handler = handler

    def on_form_closed(self, e):
        self.ex_event.Dispose()
        self.ex_event = None
        self.handler = None

        super(on_form_closed(e))

    def close_button_click(self, sender, e):
        self.Close()

    def show_messagebutton_click(self, sender, e):
        self.ex_event.Raise()





