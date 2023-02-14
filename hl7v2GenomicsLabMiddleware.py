import hl7
import os
import hl7update
import datetime
from hl7v2GenomicsExtractor import Converter

cwd = os.getcwd()
print(str(datetime.datetime.now()) + "\n")

def main():

    order_filename = os.getenv("order_filename")
    filename = os.getenv("filename")

    ref_build = os.getenv("ref_build")
    patient_id = int(os.getenv("patient_id"))
    seed = int(os.getenv("seed"))
    source_class = os.getenv("source_class")
    variant_analysis_method = os.getenv("variant_analysis_method")
    
    plm = os.getenv("plm")
    accessionId = os.getenv("accessionId")
    Perc_Target_Cells = os.getenv("Perc_Target_Cells")
    Perc_Tumor = os.getenv("Perc_Tumor")
    output_filename = os.getenv("output_filename")

    allhl7filenames = [order_filename]

    for hl7_file_name in allhl7filenames:
        try:
            hl7file = open(hl7_file_name, mode="r").read()
        except:
            continue
        
        arr = hl7file.split("\n\n")

        for hl7msg in arr: 
            if hl7msg:
                msg_unix_fmt = hl7msg.replace("\n","\r")
                h = hl7.parse(msg_unix_fmt)

                if os.path.isfile(os.path.join(cwd, order_filename)) and os.path.isfile(os.path.join(cwd, filename)):
                    if os.path.isfile(os.path.join(cwd, filename)):

                        genes_list, diagnosis = hl7update.find_genes_from_XML(filename)
                        gene_map={}

                        if genes_list:
                            for gene in genes_list:
                                x = gene.split(" ", 1)
                                if x[0] in gene_map.keys():
                                    gene_map[x[0]].append(x[1])
                                else:
                                    gene_map[x[0]] = [x[1]]

                        current_date = hl7update.get_current_formatted_date()

                        hl7update.update_msh_segment(h, current_date)
                        hl7update.update_orc_segment(h)
                        hl7update.update_obr_segment(h, current_date)

                        out_file_path = f'{cwd}/hl7-{plm}-output.txt'
                        if h:
                            conv = Converter(filename=filename, ref_build=ref_build,
                                             patient_id=patient_id, seed=seed,
                                             source_class=source_class,
                                             variant_analysis_method=variant_analysis_method)

                            hl7_v2_message = conv.convert(output_filename)

                            obx_segments = []
                            for segment in hl7_v2_message.obx:
                                obx_segments.append(segment.to_er7().replace("\R\\", "~"))

                            obx_segments = hl7update.append_additional_OBX_segments(current_date, obx_segments, str(plm), accessionId, diagnosis, Perc_Target_Cells, Perc_Tumor, genes_list)
                            obx_segments_string = "\n".join(obx_segments)

                            with open(out_file_path, 'w' ,  encoding='utf-8') as f:
                                f.write(str(h))
                                f.write("\n")
                                f.write(obx_segments_string)
                            print("Out file available at :",out_file_path)
 
                        else:
                            print("Couldn't replace '-' in hl7. Check logs for more details!")
                    else:
                        print("XML was not yet generated for the  " + accessionId)

main()
