const testsList = document.getElementById("testsList");




document.getElementById("createTestButton").querySelector("img").addEventListener("click", () => createTest() );
  document.getElementById("sendDataButton").addEventListener("click", sendData);



function sendData() {
let xhr = new XMLHttpRequest();
let url = "DataProccesor";
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.send(collectDataToJson());
}

function adjustInputFieldSize() {
  let label = document.getElementById("searchInputField");
  if (label.value.length > 5) {
     label.cols = label.cols + 1;
  }
}

function collectDataToJson() {
  data = new Object();
  data.searchRequest = document.getElementById("search").querySelector("textarea").value;
  data.tests = new Array();

  let testsCases = document.getElementById("testsList").getElementsByClassName("testCase");

  for (let testCase of testsCases) {
    let test = {
        "name": testCase.querySelector(".testName").querySelector("input").value,
        "result": testCase.querySelector(".testCaseResult").querySelector("input").value
    };

    test.arguments = new Array();
    testInputs = testCase.querySelector(".testCaseArgument").getElementsByTagName('input');
    for (let testInput of testInputs) {
      test.arguments.push(testInput.value);
    }
    data.tests.push(test);
  }
  return JSON.stringify(data);
}


function createArgument(button) {
  let argumentsWindow = button.parentNode.parentNode.nextElementSibling.querySelector(".testCaseArgument");
  let input = document.createElement("input");
  input.setAttribute("type", "text");
  argumentsWindow.appendChild(input);
  input.focus();
  event.stopPropagation();

}

function toggleTestsWindow(test) {
  if (test.nextElementSibling.style.display == "none") {
    test.nextElementSibling.style.display = "block";
    test.querySelector(".createTestCaseButton").style.display = "block";
  }
  else {
    test.nextElementSibling.style.display = "none";
    test.querySelector(".createTestCaseButton").style.display = "none";
  }
}

function createTest() {
  let testsList = document.getElementById("testsList");

  let testCase = document.createElement("div");
  testCase.setAttribute("class", "testCase");

  let testName = document.createElement('div');
  testName.setAttribute('class', 'testName');
  testName.addEventListener("click", function () {
    toggleTestsWindow(this);
  });
  testCase.appendChild(testName);



  let test = document.createElement("div");
  test.setAttribute("class", "test");
  testCase.appendChild(test);
  testsList.appendChild(testCase);


  let input = document.createElement("input");
  input.setAttribute("type", "text");
  testName.appendChild(input);

  let createTestCaseButton = document.createElement('div');
  createTestCaseButton.setAttribute('class', 'createTestCaseButton')
  testName.appendChild(createTestCaseButton);

  let img = document.createElement("img");
  img.setAttribute("src", "resources/btn2.png");
  img.addEventListener("click", function () {
    createArgument(this)
  });
  createTestCaseButton.appendChild(img);


  let wrapper = document.createElement("div");
  wrapper.setAttribute("class", "wrapper");
  test.appendChild(wrapper);

  let testCaseArgument = document.createElement('div');
  testCaseArgument.setAttribute("class", "testCaseArgument");
  testCaseArgument.innerHTML = "<span>"+ "argument" +"</span>";
  wrapper.appendChild(testCaseArgument);

  let testCaseResult = document.createElement('div');
  testCaseResult.setAttribute("class", "testCaseResult");
  testCaseResult.innerHTML = "<span>"+ "result" +"</span>";

  let resultInput = document.createElement("input");
  resultInput.setAttribute("type", "text");
  testCaseResult.appendChild(resultInput);

  wrapper.appendChild(testCaseResult);

  input.focus();
}
