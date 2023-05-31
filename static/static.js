const submitExpressionBtn = document.getElementById("submitExpressionBtn");
const clearBtn = document.getElementById("clearExpressionList");
const graphImageDiv = document.getElementById("graphImageDiv");
const dropZone = document.getElementById("dropZone");
const expressionInput = document.getElementById("expressionInput");
const expressionNameInput = document.getElementById("expressionNameInput");
console.log(expressionNameInput);
const saveExpressionCheckbox = document.getElementById("myCheckbox");
let expression = "";
let columnDropped = false;
let expressionName = "";

document.getElementById("file-input").addEventListener("change", function () {
  document.getElementById("upload-form").submit();
});

if (expression === "") {
  clearBtn.style.display = "none";
  graphImageDiv.style.display = "none";
}

dropZone.addEventListener("dragover", function (event) {
  event.preventDefault();
});

dropZone.addEventListener("drop", function (event) {
  event.preventDefault();
  const draggedData = event.dataTransfer.getData("text/plain").trim(); // Remove leading/trailing spaces
  const dataType = event.dataTransfer.getData("data-type");

  expression += draggedData;
  expressionInput.value = expression;
  console.log(expression);
  console.log(expressionInput);

  if (expression !== "") {
    clearBtn.style.display = "initial";
  } else {
    clearBtn.style.display = "none";
  }

  expressionInput.value = expression; // Update the expression in the text input
});

expressionInput.addEventListener("input", function (event) {
  const inputText = event.target.value; // Remove leading/trailing spaces
  expression = inputText;
});

function drag(event) {
  event.dataTransfer.setData("text/plain", event.target.textContent);
  event.dataTransfer.setData("data-type", event.target.getAttribute("data-type"));
}

function clearExpressionList() {
  expression = "";
  columnDropped = false;
  expressionInput.value = "";
}

submitExpressionBtn.addEventListener("click", function () {
  // Send the expression list to the backend
  expressionName = expressionNameInput.value;
  submitExpressionList(expression, expressionName);
  clearBtn.style.display = "none";
  graphImageDiv.style.display = "flex";
  expressionNameInput.value = "";
});

async function submitExpressionList(expression, expressionName) {
  const csrfToken = getCookie("csrftoken");

  try {
    const response = await fetch("/submit-expression", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ expressionList: expression, expressionName: expressionName }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    const plotHtml = data.plot_html;

    // Get the expression div element
    const expressionDiv = document.getElementById("expressionDiv");

    // Get the iframe element
    const iframe = document.getElementById("graph-iframe");

    // Set the HTML content of the iframe
    iframe.contentDocument.open();
    iframe.contentDocument.write(plotHtml);
    iframe.contentDocument.close();

    // Clear the expression list and reset variables
    clearExpressionList();
  } catch (error) {
    console.error("Error:", error);
  }
}

// Get CSRF token from cookies
function getCookie(name) {
  const cookieValue = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
  return cookieValue ? cookieValue.pop() : "";
}
