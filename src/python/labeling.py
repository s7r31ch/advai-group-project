from tools.LabelAssistant import LabelAssistant

label_assistant = LabelAssistant("./src/resources/downcam", "./src/ryesources/category.csv")
label_assistant.start()