<template>
  <div class="p-4">
    <!-- Inputs for CSV Paths -->
    <div class="mb-4">
      <label class="block text-white">Input CSV Path:</label>
      <input
        v-model="inputCsvPath"
        class="w-full p-2 bg-gray-700 text-white rounded"
        placeholder="Enter input CSV path"
      />
    </div>
    <div class="mb-4">
      <label class="block text-white">Output CSV Path:</label>
      <input
        v-model="outputCsvPath"
        class="w-full p-2 bg-gray-700 text-white rounded"
        placeholder="Enter output CSV path"
      />
    </div>

    <!-- Code Display with Line Numbers and Scroll -->
    <pre class="language-python rounded-lg overflow-y-auto max-h-96 p-4 bg-gray-800 text-gray-200">
      <code v-html="codeWithLineNumbers"></code>
    </pre>

    <!-- Download Button -->
    <button @click="downloadModifiedFile" class="mt-4 px-4 py-2 bg-green-500 text-white rounded-lg">
      Download Python File
    </button>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import Prism from "prismjs";
import "prismjs/components/prism-python";

export default {
  setup() {
    const codeContent = ref("");
    const inputCsvPath = ref("anki-new-word.csv");
    const outputCsvPath = ref("output.csv");

    const loadFile = async () => {
      try {
        const response = await fetch("/pythonFile.py");
        codeContent.value = await response.text();
      } catch (error) {
        console.error("Error loading file:", error);
      }
    };

    const codeWithLineNumbers = computed(() => {
      const modifiedCode = codeContent.value
        .replace(/input_csv = '.*'/, `input_csv = '${inputCsvPath.value}'`)
        .replace(/output_csv = '.*'/, `output_csv = '${outputCsvPath.value}'`);
        
      return modifiedCode
        .split("\n")
        .map((line, index) => {
          const lineNumber = `<span class="text-gray-500 select-none">${index + 1}</span>`;
          const highlightedLine = Prism.highlight(line, Prism.languages.python, "python");
          return `${lineNumber} ${highlightedLine}`;
        })
        .join("\n");
    });

    const downloadModifiedFile = () => {
      const modifiedCode = codeContent.value
        .replace(/input_csv = '.*'/, `input_csv = '${inputCsvPath.value}'`)
        .replace(/output_csv = '.*'/, `output_csv = '${outputCsvPath.value}'`);
      
      const element = document.createElement("a");
      element.setAttribute(
        "href",
        "data:text/plain;charset=utf-8," + encodeURIComponent(modifiedCode)
      );
      element.setAttribute("download", "modified_pythonFile.py");
      element.style.display = "none";
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    };

    onMounted(() => {
      loadFile();
    });

    return {
      inputCsvPath,
      outputCsvPath,
      codeWithLineNumbers,
      downloadModifiedFile,
    };
  },
};
</script>

<style>
@import "prismjs/themes/prism-tomorrow.css"; /* Customize as needed */
</style>
