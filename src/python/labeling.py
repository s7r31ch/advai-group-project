from tools.LabelAssistant import LabelAssistant

label_assistant = LabelAssistant("src/resources/record_downcam", "src/resources/category.csv")
label_assistant.start()