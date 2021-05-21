# -*- coding: utf8 -*-
import os

from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
from jinja2 import Template


# reading data from a file config.cfg
def read_db_config(filename='config.cfg', section='mysql'):
	parser = ConfigParser()
	parser.read(filename)
 
	db = {}
	if parser.has_section(section):
		items = parser.items(section)
		for item in items:
			db[item[0]] = item[1]
	else:
		raise Exception('{0} not found in the {1} file'.format(section, filename))
	return db


# data read request
def execute_read_query(connection, query) :
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		result = cursor.fetchall()
		return result
	except Error as e :
		print(f"The error '{e}' occurred")


# execution request
def execute_query(connection, query) :
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		connection.commit()
	except Error as e:
		print(f"The error '{e}' occurred")


# search function
def func_search(ext) :
	result = list()
	for file in os.listdir("."):
		if file.endswith(ext):
			result.append(file)
	return result


if __name__ == '__main__':

	# database connections
	db_config = read_db_config()
	try:
		connection = MySQLConnection(**db_config)

	except Error as e :
		print(f"The error '{e}' occurred")
		raise
	
	# creating and opening a file for reading
	html_file = open('IPTV_report.html','w')

	# grouping request for id channels
	query = f"""
	SELECT id_channel_f 
	FROM data_video 
	GROUP BY id_channel_f
	"""
	query_select_id_channel_f_1 =  execute_read_query(connection, query)	
	
	for id_ in query_select_id_channel_f_1:
		# heading
		query = f"""
		SELECT name_channel 
		FROM channels_name 
		WHERE id_channel = {id_[0]}
		"""
		query_select_id_channel_f_2 =  execute_read_query(connection, query)
		heading = query_select_id_channel_f_2[0][0]

		# table
		query = f"""
		SELECT sum_error, date 
		FROM data_video
		WHERE id_channel_f = {id_[0]}
		ORDER BY date
		"""
		query_select_id_channel_f_3 =  execute_read_query(connection, query)

		# create html
		template = Template('''
		<table cellspacing="2" border="0" cellpadding="5" style="display:inline">
			<tr><th colspan="2"> {{ heading }} </th></tr>
			{% for i in query_select_id_channel_f_3 %}
			<tr>
				{% if i[0] == 0 %}
				<td style ="background-color: white"> {{i[0]}} </td> <td style ="background-color: white"> {{i[1]}} </td>
				{% elif 15 > i[0] > 0 %}
				<td style ="background-color: green"> {{i[0]}} </td> <td style ="background-color: green"> {{i[1]}} </td>
				{% elif 30 > i[0] > 15 %}
				<td style ="background-color: yellow"> {{i[0]}} </td> <td style ="background-color: yellow"> {{i[1]}} </td>
				{% else %}
				<td style ="background-color: red"> {{i[0]}} </td> <td style ="background-color: red"> {{i[1]}} </td>
				{% endif %}    
			</tr>
			{% endfor %}
		</table>
		''')

		# output html
		output = template.render(query_select_id_channel_f_3=query_select_id_channel_f_3, heading=heading)
		html_file.write(output)
	
	# disconnecting from the database
	connection.close()