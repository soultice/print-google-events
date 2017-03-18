import PrintMode
import Events
import Tasks
import subprocess
import PrinterConnector

if __name__ == "__main__":
    putter = PrintMode.ImgCreator()
    events = Events.EventGetter()
    printer = PrinterConnector.PrinterConnector()

    url_auth ='https://accounts.google.com/ServiceLoginAuth'
    url_login = 'https://accounts.google.com/ServiceLogin'

    task_session = Tasks.SessionGoogle(url_login, url_auth,
            'florian.pfingstag@gmail.com', 'armageddon!')
    task_session.get('http://keep.google.com/#reminders')
    task_session.get_page_text()
    task_session.parse_json()
    reminders = task_session.get_reminders()
    text = events.get_next_events()
     
    events_text = [[k, v] for k, v in text.items()]
    events_text = sorted(events_text, key=lambda x: x[0])
    events_text = [events_text] + [reminders] + ['']

    putter.put_all_boxes()
    putter.put_all_text(events_text)
    putter.save_img('printbuffer.png')
    
    printer.print_file('Muenchen_Haus', 'printbuffer.png')
