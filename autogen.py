import cantools
import math

def build_name(name):
    nodes = name.split("_")
    nodes[0] = nodes[0].title()
    return "".join(nodes)

def signal_variable_name(signal_name):
    return "m_" + build_name(signal_name)

def isFloat(signal):
    return True if isinstance(signal.scale, float) else False

def signal_data_type(signal):
    if not signal.choices:
        if isFloat(signal):
            return "float"
        else:
            return "int" if signal.is_signed else "uint" + str((math.floor((signal.length - 1) / 8) + 1) * 8) + "_t"
    else:
        return signal.name

def initial_signal_value(signal):
    initial = 0
    if signal.initial:
        initial = signal.initial
    print("initial: "+str(initial))
    print(signal.choices)
    if signal.choices:
        return signal.name + "_" + signal.choices[initial]
    else:
        return initial

cpp_template = """
#include <string>

#include "{messagename}.h"

using namespace std;

{messagename}::{messagename}()
{{
}}

"""
header_template = """
#ifndef {message_h}
#define {message_h}

#include <stdint.h>
#include <iostream>

class {messagename} : public {messageparent} {{
public:
    {messagename}();

    bool processMessage();

private:
"""

# dbc file 
db = cantools.database.load_file("file2.dbc")

# We can grow following list, add those messages for which we want to generate the code. 
messages_list=["INIT_FB","MOTOR_OUT_ELEC","MOTOR_OUT_MEC","MOTOR_ANGLE_SP"]

for message_name in messages_list:
    print(message_name)
    # massaging message_name here. 
    good_message_name = build_name(message_name)
    message = db.get_message_by_name(message_name)
    message_cpp_file = good_message_name+".cpp"
    context = {"messagename": good_message_name, "dbc_message_name": message_name}

    # writing code for C++ file.
    f = open(message_cpp_file, "w")
    f.write(cpp_template.format(**context))
    f.write("bool {}::processMessage() {{\n    return true;\n}}\n".format(good_message_name))
    # we can add more code here to auto-generate code inside above fucntion to process the signals.
    f.close()

    # writing code for header file.
    message_header_file = good_message_name+".h"
    f = open(message_header_file, "w")
    context["message_h"] = message_name.upper()+"_H"
    context["messageparent"] = "ProcessMessageInterface"
    f.write(header_template.format(**context))

    for signal in message.signals:
        f.write("    {} {};\n".format(signal_data_type(signal), signal_variable_name(signal.name)))

    f.write("\n};\n\n#endif // " + context["message_h"])
    f.write("\n")
    f.close()
