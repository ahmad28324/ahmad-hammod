from wsgiref.simple_server import make_server
import sys
from urllib.parse import parse_qs
from datetime import datetime
import dateutil.parser
from pytz import timezone
import pytz
import json

#This function returns the current time in the given timezone timez
def get_current(timez):
  try:
    time_tz = timezone(timez)
    dt = datetime.now().astimezone(time_tz) #timezone

    fmt = '%m.%d.%Y %H:%M:%S %Z' #Format for printing
    return 'Current Time of '+timez+' is: '+dt.strftime(fmt)
  except:
    return print("Couldn't get the Date Time. Something wrong: ", sys.exc_info()[0])
    raise

#This function takes a datatime with its zone in json format, And takes another timezone and returns the datetime in the other timezone
def convert_dt(dt_json , new_tz):
  #Read the date json content
  old_date = ''
  old_tz = ''
  data_date = json.loads(dt_json)
  for key, value in data_date.items():
    if(key == 'date'):
      old_date = value;
    if(key == 'tz'):
      old_tz = value
  fmt = '%m.%d.%Y %H:%M:%S'
  dt_old = timezone(old_tz).localize(datetime.strptime(old_date,fmt))
  dt_new = dt_old.astimezone(timezone(new_tz))
  return dt_new.strftime(fmt)

#This function calculates the time difference between two different dates in seconds
def diff_date(dates_json):
  #Read the date json content
  first_date = ''
  first_tz = ''
  second_date = ''
  second_tz = ''
  data_date = json.loads(dates_json)
  for key, value in data_date.items():
    if(key == 'first_date'):
      first_date = value;
    if(key == 'second_date'):
      second_date = value
    if(key == 'first_tz'):
      first_tz = value;
    if(key == 'second_tz'):
      second_tz = value
  dt_first= timezone(first_tz).localize(dateutil.parser.parse(first_date))
  dt_second= timezone(second_tz).localize(dateutil.parser.parse(second_date))

  #Convert the datetimes to GMT
  dt_first_gmt = dt_first.astimezone(timezone('GMT'))
  dt_second_gmt = dt_second.astimezone(timezone('GMT'))
  #The difference between datetimes in seconds
  return (dt_first_gmt-dt_second_gmt).total_seconds()


#Web Application Method
def application (environ, start_response):

    get_data = parse_qs(environ['QUERY_STRING'])
    current_time = get_current('Etc/GMT')

    #Selected timezone sent by GET request
    tz_selected = get_data.get('tz', [''])[0] 

    #The post request
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    post_data = parse_qs(request_body.decode())

    #post_input = parse_qs(environ['wsgi.input'].readline().decode(),True)
    dt_post = post_data.get('dt_sel', [''])[0] # Returns the selected date time for converting
    new_tz_post = post_data.get('new_tz', [''])[0] # Returns the targeted timezone
    if(dt_post != ""):
      resulted_time = convert_dt(dt_post , new_tz_post)
    else:
      resulted_time = ''

    dtdiff_post =post_data.get('dtdiff_post', [''])[0] # Returns the selected date times for Difference Calculation
    if(dtdiff_post != ""):
      diff_result = diff_date(dtdiff_post)
    else:
      diff_result = ''
    if(tz_selected != ''):
      current_time = get_current(tz_selected)
    html = """
      <html>
      <body>
 <select id="tz_select" >
	<option disabled selected style='display:none;'>Time Zone...</option>
	<optgroup label="US (Common)">	
		<option value="America/Puerto_Rico">Puerto Rico (Atlantic)</option>
		<option value="America/New_York">New York (Eastern)</option>
		<option value="America/Chicago">Chicago (Central)</option>
		<option value="America/Denver">Denver (Mountain)</option>
		<option value="America/Phoenix">Phoenix (MST)</option>
		<option value="America/Los_Angeles">Los Angeles (Pacific)</option>
		<option value="America/Anchorage">Anchorage (Alaska)</option>
		<option value="Pacific/Honolulu">Honolulu (Hawaii)</option>
	</optgroup>
	<optgroup label="Europe">
		<option value="Europe/Amsterdam">Amsterdam</option>
		<option value="Europe/Andorra">Andorra</option>
		<option value="Europe/Athens">Athens</option>
		<option value="Europe/Berlin">Berlin</option>
		<option value="Europe/Copenhagen">Copenhagen</option>
		<option value="Europe/Dublin">Dublin</option>
		<option value="Europe/Gibraltar">Gibraltar</option>
		<option value="Europe/Guernsey">Guernsey</option>
		<option value="Europe/Helsinki">Helsinki</option>
		<option value="Europe/Isle_of_Man">Isle of Man</option>
		<option value="Europe/Istanbul">Istanbul</option>
		<option value="Europe/Lisbon">Lisbon</option>
		<option value="Europe/Ljubljana">Ljubljana</option>
		<option value="Europe/London">London</option>
		<option value="Europe/Luxembourg">Luxembourg</option>
		<option value="Europe/Madrid">Madrid</option>
		<option value="Europe/Minsk">Minsk</option>
		<option value="Europe/Moscow">Moscow</option>
		<option value="Europe/Paris">Paris</option>
		<option value="Europe/Riga">Riga</option>
		<option value="Europe/Rome">Rome</option>
		<option value="Europe/Samara">Samara</option>
		<option value="Europe/San_Marino">San Marino</option>
		<option value="Europe/Sarajevo">Sarajevo</option>
		<option value="Europe/Simferopol">Simferopol</option>
		<option value="Europe/Skopje">Skopje</option>
		<option value="Europe/Sofia">Sofia</option>
		<option value="Europe/Stockholm">Stockholm</option>
		<option value="Europe/Tallinn">Tallinn</option>
		<option value="Europe/Tirane">Tirane</option>
		<option value="Europe/Tiraspol">Tiraspol</option>
		<option value="Europe/Uzhgorod">Uzhgorod</option>
		<option value="Europe/Vaduz">Vaduz</option>
		<option value="Europe/Vatican">Vatican</option>
		<option value="Europe/Vienna">Vienna</option>
		<option value="Europe/Vilnius">Vilnius</option>
		<option value="Europe/Volgograd">Volgograd</option>
		<option value="Europe/Warsaw">Warsaw</option>
		<option value="Europe/Zagreb">Zagreb</option>
		<option value="Europe/Zaporozhye">Zaporozhye</option>
		<option value="Europe/Zurich">Zurich</option>
	</optgroup>
</select>
<button onclick="refreshWithZone()">Get Time</button>
<p>
      %(current_time)s
</p>
<hr>
        <form method="post" action="">
        <p>
        Date & Time & Timezone in JSON Format:
        <input type="text" size="30" id="dt_sel" name="dt_sel" for="dt_sel"><br/>
        Target Time Zone: <input type="text" id="new_tz"  value = "%(new_tz_post)s" for="new_tz" name="new_tz"><br/>
        %(dt_post)s <br/>
        <b>Converssion Result: %(resulted_time)s</b>
        </p>
              <p>
                  <input type="submit" value="Convert">
              </p>
          </form>
<hr>
        <form method="post" action="">
        <p>
        Date1 & Time1 & Timezone1 & Date2 & Time2 & Timezone2 in JSON Format:
        <input type="text" size="50" id="dtdiff_post"  name="dtdiff_post" for="dtdiff_post"><br/>
        </p>
              <p>
                  <input type="submit" value="Calculate">
              </p>
              %(dtdiff_post)s
              <b>Difference in Seconds is: %(diff_result)s</b>
          </form>
<script>
function refreshWithZone() {
  var sel = document.getElementById("tz_select");
  location.replace(window.location.hostname+'?tz='+sel.options[sel.selectedIndex].value);
}
</script> 
      </body>
      </html>
      """

    response_body = html % { # Fill the above html 
        'current_time' : current_time or '',
        'dt_post' : dt_post or '',
        'dtdiff_post' : dtdiff_post or '',
        'resulted_time' : resulted_time or '',
        'new_tz_post' : new_tz_post or '',
        'diff_result' : diff_result or ''
       
    }

    status = '200 OK'

    # Now content type is text/html
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body.encode()]

with make_server('', 8080, application) as httpd:
    print("Serving on port 8009...")
    httpd.serve_forever()
    httpd.handle_request()