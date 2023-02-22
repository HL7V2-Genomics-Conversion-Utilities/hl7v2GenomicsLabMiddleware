import hl7apy.core as hl7
import pandas as pd
import os

def main():

	hl7_filename = os.getenv("hl7_filename")
	excel_filename = os.getenv("excel_filename")

	obx_segments_to_add = hl7.Message("ORU_R01")

	with open(hl7_filename) as f:
		message = f.readlines()
	
	last_obx_index = int(message[-1].split("|")[1])

	start_from_index = last_obx_index + 1

	additional_lab_values = pd.read_excel(excel_filename)

	for lab_value in additional_lab_values:
		key = lab_value
		value = additional_lab_values[lab_value][0]
		print(key, value)
		if not pd.isnull(value):
			obx = hl7.Segment("OBX")
			obx.obx_1 = str(start_from_index)
			obx.obx_2 = "ST"
			obx.obx_3 = str(key)
			obx.obx_4 = '3'
			obx.obx_5 = str(value)
			obx_segments_to_add.add(obx)
			start_from_index += 1

	with open(hl7_filename, 'a', encoding='utf-8') as output_file:
		output_file.write('\n')
		for segment in obx_segments_to_add.obx:
			print(segment)
			output_file.write(segment.to_er7().replace(r"\R\\", "~"))
			output_file.write('|\n')

main()
