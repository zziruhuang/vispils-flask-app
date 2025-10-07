console.log("main.js loaded and running!");

// import { postRequestJSON } from './request.js';

const endPoint = "http://127.0.0.1:5001/api/selection";
const endPoint1 = "http://127.0.0.1:5001/api/ionic-liquid";

// add click events for all options
$(function () {
  $(".option").on("click", function () {
    // Deselect all options in the current selection container
    $(this)
      .closest(".selection-container")
      .find(".option")
      .removeClass("selected");
    $(this).addClass("selected");
    var selectBtn = $(this).parents(".selection-container").find(".select-btn");
    selectBtn.addClass("active");
    selectBtn.off("click").on("click", confirmSelection);
  });
});

function SelectOption() {
  $(this).addClass("selected").siblings().removeClass("selected");

  // if user has selected, allow re-selection by not disabling others
  // const currentSection = $(this).parents(".selection-container");
  // currentSection.find(".option").not(".selected").addClass("disabled");

  // make a request to the python backend by clicking on SUBMIT
  var selectBtn = $(this).parents(".selection-container").find(".select-btn");
  selectBtn.addClass("active");
  selectBtn.off("click").on("click", confirmSelection);
}

let finalSelection = {};

// Predict IL properties by sending SMILES and temperature to backend
async function predictILProperties(smiles, temperature) {
  const formData = new FormData();
  formData.append("SMILES_input", smiles);
  formData.append("Temperature_input", temperature);

  return fetch("http://127.0.0.1:5001/api/predict", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .catch((error) => {
      console.error("Prediction request failed:", error);
      return { success: false, error: error.toString() };
    });
}

async function confirmSelection() {
  const currentSection = $(this).parents(".selection-container");
  // retrieve the selection
  const userSelection = currentSection.find(".selected").attr("value");

  let userSelectedEntry = {};
  userSelectedEntry[currentSection.attr("id")] = userSelection;

  // make a request to the python backend
  const dataImgs = await postRequestJSON(endPoint, userSelectedEntry);

  // if success: try{}catch(error){console.error}
  finalSelection[currentSection.attr("id")] = userSelection;
  console.log(finalSelection);

  // jump to the next container
  const nextContainer = currentSection.next();

  if ($(this).attr("id") == "btn4") {
    const selected_il = await postRequestJSON(endPoint1, finalSelection);
    $(".final-selection").addClass("active");

    // Construct IL SMILES
    const ilSmiles =
      finalSelection["select-cations"] + "." + finalSelection["select-anions"];
    // Get temperature from user input (assume input exists)
    const temperature = $("#temperature-input").val();
    console.log("IL SMILES:", ilSmiles, "Temperature:", temperature);

    // Show 'Predicting...' in the results section
    $("#results_section .results-title").text(
      "Predicted & Experimental Properties"
    );
    $("#results_section .results-description").html(
      '<span style="color:var(--text-secondary)">Predicting...</span>'
    );
    $("#results_section").show();
    // Also show 'Predicting...' below the submit button
    $("#stepwise-smiles-result").html(
      '<span style="color:var(--text-secondary)">Predicting...</span>'
    );

    // Call prediction
    const predictionResult = await predictILProperties(ilSmiles, temperature);
    console.log("Prediction result:", predictionResult);

    // Display result
    if (predictionResult.success) {
      renderPredictionResult(predictionResult);
      $("#stepwise-smiles-result").html(""); // Clear the predicting text
    } else {
      $("#stepwise-smiles-result").html(
        `<span style="color:red">${
          predictionResult.error || "Prediction failed."
        }</span>`
      );
      alert(
        "Prediction failed: " + (predictionResult.error || "Unknown error")
      );
    }

    // Existing code for JSmol, etc.
    $(".final-selection").text("3D Structure of Your Selected Ionic Liquid");
    $(".viewer-description").text(
      "Visualize the predicted or experimental structure below."
    );
    const jsmolScript = writeJsmolScript(selected_il.ionic_liquid);
    $("#JmolDiv").append(jsmolScript);

    // Show both results and viewer sections, and scroll to results first, then viewer
    showOnlyStep("results_section");
    $("#results_section").show();
    $("#viewer_section").show();
    syncProgressBar("results_section");
    document
      .getElementById("results_section")
      .scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  } else {
    showOnlyStep(nextContainer.attr("id"));
    syncProgressBar(nextContainer.attr("id"));
    location.href = "#" + nextContainer.attr("id");
    // display the mols from reply
    // const ionsBox = nextContainer.children(".mol-list");
    // ionsBox.empty(); // Clear previous mols to start a new row

    var querySet = {
      queryData: dataImgs["candidates"],
      NumMols: 45,
    };

    querySet["queryDataHTML"] = querySet["queryData"].map((values) => {
      var valueHTML = `<div class="mol-imgs" value=${values.smiles}>
                                <img src="${values.image_url}"></img>
                                </div>`;
      return valueHTML;
    });

    // Map selection step to the container to populate
    const stepToContainer = {
      "select-cfams": "#select-cations .mol-list",
      "select-afams": "#select-anions .mol-list",
      // Add more if needed
    };
    const currentStep = currentSection.attr("id");
    const targetMolList = $(stepToContainer[currentStep]);
    // Remove only dynamic mols, keep static examples
    targetMolList.find(".mol-imgs:not(.static-mol-imgs)").remove();
    displayMolImgs(querySet.queryDataHTML, querySet.NumMols, targetMolList);

    // Always set up click handlers for all .mol-imgs (static and dynamic)
    $(".mol-imgs")
      .off("click")
      .on("click", function () {
        $(this).addClass("selected").siblings().removeClass("selected");
        var selectBtn = $(this)
          .parents(".selection-container")
          .find(".select-btn");
        selectBtn.addClass("active");
        selectBtn.off("click").on("click", confirmSelection);
      });

    // Re-attach page button event handlers after dynamic population
    $(document)
      .off("click", ".mol-list-page-btn")
      .on("click", ".mol-list-page-btn", function () {
        const position = $(this)
          .closest(".selection-container")
          .find(".mol-list");
        position.empty();
        const page = $(this).val();
        const slicedHTML = position.data("slicedHTML");
        if (slicedHTML && slicedHTML[page]) {
          position.append(slicedHTML[page]);
        }
        // Re-attach click handlers for new .mol-imgs
        $(".mol-imgs")
          .off("click")
          .on("click", function () {
            $(this).addClass("selected").siblings().removeClass("selected");
            var selectBtn = $(this)
              .parents(".selection-container")
              .find(".select-btn");
            selectBtn.addClass("active");
            selectBtn.off("click").on("click", confirmSelection);
          });
      });
  }
}

function writeJsmolScript(molData) {
  const molFile = molData["molfile_3d"];
  console.log("molData:", molData);
  console.log("molFile for JSmol:", molFile);

  // Defensive: If molFile is undefined or empty, show an error
  if (!molFile || typeof molFile !== "string" || molFile.trim() === "") {
    alert("No valid MOL file received for JSmol visualization.");
    return "";
  }

  const jsmolScript = `<script>
    drawSmiles_jmol();
    function drawSmiles_jmol() {
      $('#JmolDiv').html(Jmol.getAppletHtml(myJmol, JmolInfo));
      try {
        var molFileData = \`${molFile}\`;
        Jmol.script(myJmol, 'load inline \"' + molFileData + '\"; ');
      } catch (error) {
        alert(error);
      }
      $("#myJmol_appletdiv").css({ width: \"100%\" });
      Jmol.jmolButton(myJmol, \"reset\", \"Reset to original orientation\");
    };
  </script>`;
  return jsmolScript;
}

// POST request: return a promise that returns a JSON
async function postRequestJSON(endPoint, data) {
  return fetch(endPoint, {
    method: "POST",
    // mode: 'no-cors',
    headers: { "Content-type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((res) => {
      if (res.ok) {
        console.log("POST request successful");
        return res.json();
      } else {
        console.log("POST request unsuccessful");
        return;
      }
    }) // check whether the POST request was succesful
    .catch((error) => console.log(error));
}

export { postRequestJSON };

function displayMolImgs(queryDataHTML, NumMols, position) {
  var pages = Math.ceil(queryDataHTML.length / NumMols);
  const slicedHTML = pagination(pages, queryDataHTML, NumMols);

  // Store the slicedHTML on the container for later access
  position.data("slicedHTML", slicedHTML);

  // show the first page
  position.append(slicedHTML[1]);

  addPageButtons(pages, slicedHTML, position);
}

function addPageButtons(pages, slicedHTML, position) {
  // add page button container
  position.after("<div class='page-btns'></div>");

  for (var page = 1; page <= pages; page++) {
    position
      .next(".page-btns")
      .append(
        `<button value=${page} class='mol-list-page-btn'>${page}</botton>`
      );
  }

  // build table on click
  $(".mol-list-page-btn").on("click", function () {
    $(position).empty();
    page = $(this).val();

    slicedHTML[page];
    position.append(imgHTML);
  });
}

function pagination(pages, queryData, NumMols) {
  var slicedData = {};

  for (var page = 1; page <= pages; page++) {
    var trimStart = (page - 1) * NumMols;
    var trimEnd = trimStart + NumMols;

    slicedData[page] = queryData.slice(trimStart, trimEnd);
  }

  return slicedData;
}

// Sync progress bar with the current selection step
function syncProgressBar(currentSectionId) {
  $(".progress-step").removeClass("active");
  $(`.progress-step[data-target='${currentSectionId}']`).addClass("active");
}

// Show only the current selection step
function showOnlyStep(stepId) {
  $(".selection-container").hide();
  $("#" + stepId).show();
}

// Make progress bar steps clickable for navigation and resubmission
$(document).on("click", ".progress-step", function () {
  const targetId = $(this).data("target");
  showOnlyStep(targetId);
  syncProgressBar(targetId);
  location.href = "#" + targetId;
  // Clear page buttons
  $(".page-btns").remove();
});

// Resubmit button logic
$(document).on("click", "#resubmit-btn", function () {
  showOnlyStep("select-cfams");
  syncProgressBar("select-cfams");
  location.href = "#select-cfams";
  // Clear page buttons
  $(".page-btns").remove();
});

// Shared function to render prediction results in the unified results panel
function renderPredictionResult(predictionResult) {
  const pred = predictionResult.prediction;
  console.log("Prediction object:", pred);
  let resultHtml = "";
  if (pred.experimental_text) {
    resultHtml += `<div><b>Experimental:</b> ${pred.experimental_text}</div>`;
  }
  if (pred.predicted_text) {
    resultHtml += `<div><b>G2CNN prediction:</b> ${pred.predicted_text}</div>`;
  }
  $("#results_section .results-title").text(
    "Predicted & Experimental Properties"
  );
  $("#results_section .results-description").html(resultHtml);
  // Calculate error if both values are present
  let error =
    typeof pred.experimental_value === "number" &&
    typeof pred.predicted_value === "number"
      ? Math.abs(pred.experimental_value - pred.predicted_value).toFixed(2)
      : "-";
  let rowHtml = `<tr>
    <td>${pred.standardized_smiles || "-"}</td>
    <td>${pred.temperature || "-"}</td>
    <td>${
      typeof pred.experimental_value === "number" &&
      !isNaN(pred.experimental_value)
        ? pred.experimental_value.toFixed(2)
        : "-"
    }</td>
    <td>${
      typeof pred.predicted_value === "number" && !isNaN(pred.predicted_value)
        ? pred.predicted_value.toFixed(2)
        : "-"
    }</td>
    <td>${error}</td>
  </tr>`;
  $("#results_section .modern-table tbody").html(rowHtml);
  $("#results_section").show();
}

// Primary SMILES prediction form handler
$(document).on("submit", "#primary-smiles-form", async function (e) {
  e.preventDefault();
  const smiles = $("#primary-smiles-input").val();
  const temperature = $("#primary-temp-input").val();
  const $result = $("#primary-smiles-result");
  $result.html(
    '<span style="color:var(--text-secondary)">Predicting...</span>'
  );

  const formData = new FormData();
  formData.append("SMILES_input", smiles);
  formData.append("Temperature_input", temperature);

  try {
    const response = await fetch("http://127.0.0.1:5001/api/predict", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    if (data.success && data.prediction) {
      renderPredictionResult(data);
      $result.html(""); // Optionally clear the quick result area
      // Scroll to results section
      document
        .getElementById("results_section")
        .scrollIntoView({ behavior: "smooth", block: "center" });
      // Request 3D molfile and display in JSmol
      try {
        const molRes = await fetch("http://127.0.0.1:5001/api/molfile3d", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ smiles }),
        });
        const molData = await molRes.json();
        if (molData.success && molData.molfile_3d) {
          $(".final-selection").text(
            "3D Structure of Your Selected Ionic Liquid"
          );
          $(".viewer-description").text(
            "Visualize the predicted or experimental structure below."
          );
          const jsmolScript = writeJsmolScript({
            molfile_3d: molData.molfile_3d,
          });
          $("#JmolDiv").empty().append(jsmolScript);
          $("#viewer_section").show();
        } else {
          $("#JmolDiv").empty();
        }
      } catch (err) {
        $("#JmolDiv").empty();
      }
    } else {
      $result.html(
        `<span style="color:red">${data.error || "Prediction failed."}</span>`
      );
    }
  } catch (err) {
    $result.html('<span style="color:red">Error connecting to backend.</span>');
  }
});
