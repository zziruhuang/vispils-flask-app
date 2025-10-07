console.log("Selection.js file loaded");
$(document).ready(function () {
  console.log("Selection.js: Document ready");
  let currentStep = 1;
  const totalSteps = 4;

  // Function to update progress indicator
  function updateProgress(step) {
    $(".progress-step").removeClass("active completed clickable");

    for (let i = 1; i <= totalSteps; i++) {
      if (i < step) {
        $(`.progress-step[data-step="${i}"]`).addClass("completed");
      } else if (i === step) {
        $(`.progress-step[data-step="${i}"]`).addClass("active");
      } else {
        $(`.progress-step[data-step="${i}"]`).addClass("clickable");
      }
    }
  }

  // Function to show specific step
  function showStep(step) {
    $(".selection-container").hide();
    const targetId = $(`.progress-step[data-step="${step}"]`).data("target");
    $(`#${targetId}`).show();
    currentStep = step;
    updateProgress(step);
  }

  // Handle progress step clicks - BIDIRECTIONAL
  $(".progress-step").on("click", function () {
    console.log("Progress step clicked:", $(this).data("step"));
    const step = parseInt($(this).data("step"));
    const isClickable =
      $(this).hasClass("clickable") ||
      $(this).hasClass("active") ||
      $(this).hasClass("completed");

    console.log("Is clickable:", isClickable);
    console.log("Classes:", $(this).attr("class"));

    if (isClickable) {
      showStep(step);
      // Smooth scroll to selection section with navbar offset
      $("html, body").animate(
        {
          scrollTop: $(".select-IL").offset().top - 100,
        },
        500
      );
    }
  });

  // Handle option selection
  $(".option").on("click", function () {
    console.log("Option clicked:", $(this).attr("value"));
    $(this).addClass("selected");
    $(this).siblings().removeClass("selected");
    $(this)
      .closest(".selection-container")
      .find(".select-btn")
      .addClass("active");
  });

  // Handle molecule selection
  $(".mol-imgs").on("click", function () {
    console.log("Molecule clicked:", $(this).attr("value"));
    $(this).addClass("selected");
    $(this).siblings().removeClass("selected");
    $(this)
      .closest(".selection-container")
      .find(".select-btn")
      .addClass("active");
  });

  // Handle continue buttons
  $(".select-btn").on("click", function () {
    if ($(this).hasClass("active")) {
      const currentContainer = $(this).closest(".selection-container");
      const nextContainer = currentContainer.next(".selection-container");

      if (nextContainer.length > 0) {
        currentContainer.hide();
        nextContainer.show();
        currentStep++;
        updateProgress(currentStep);

        // Smooth scroll to selection section with navbar offset
        $("html, body").animate(
          {
            scrollTop: $(".select-IL").offset().top - 100,
          },
          500
        );
      }
    }
  });

  // Handle final generation
  $("#btn4").on("click", function () {
    if ($(this).hasClass("active")) {
      $("#select-anions").hide();
      $("#viewer_section").show();
      $("#results_section").show();

      $("html, body").animate(
        {
          scrollTop: $("#results_section").offset().top - 100,
        },
        500
      );
    }
  });

  // Handle "Start Building" button click
  $(".hero-btn.primary").on("click", function (e) {
    e.preventDefault();
    // Smooth scroll to selection section with navbar offset
    $("html, body").animate(
      {
        scrollTop: $(".select-IL").offset().top - 100,
      },
      800
    );
  });

  // Smooth scrolling for navigation
  $('a[href^="#"]').on("click", function (e) {
    e.preventDefault();
    const target = $(this.getAttribute("href"));
    if (target.length) {
      $("html, body").animate(
        {
          scrollTop: target.offset().top - 100,
        },
        500
      );
    }
  });

  // Initialize progress indicator
  updateProgress(1);
});

// Viewer control functions
function rotateMolecule() {
  console.log("Rotating molecule...");
  // Add JSmol rotation logic here
  if (typeof Jmol !== "undefined") {
    Jmol.script(myJmol, "rotate x 90");
  }
}

function zoomIn() {
  console.log("Zooming in...");
  if (typeof Jmol !== "undefined") {
    Jmol.script(myJmol, "zoom 1.5");
  }
}

function zoomOut() {
  console.log("Zooming out...");
  if (typeof Jmol !== "undefined") {
    Jmol.script(myJmol, "zoom 0.7");
  }
}

function resetView() {
  console.log("Resetting view...");
  if (typeof Jmol !== "undefined") {
    Jmol.script(myJmol, "reset");
  }
}

// Make functions globally available
window.rotateMolecule = rotateMolecule;
window.zoomIn = zoomIn;
window.zoomOut = zoomOut;
window.resetView = resetView;
