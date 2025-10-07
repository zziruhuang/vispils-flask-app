let cationFamilies = [
  {
    Name: "Unsaturated cyclic amines",
    Values: ["im", "py"],
    Labels: ["[im]", "[py]"],
    Imgs: ["../static/img/im.png", "../static/img/py.png"],
  },
  {
    Name: "Cyclic amines",
    Values: ["pyr", "pip", "mor"],
    Labels: ["[pyr]", "[pip]", "[mor]"],
    Imgs: [
      "../static/img/pyr.png",
      "../static/img/pip.png",
      "../static/img/mor.png",
    ],
  },
  {
    Name: "Acyclic",
    Values: ["s", "n", "p"],
    Labels: ["[s]", "[n]", "[p]"],
    Imgs: ["../static/img/s.png", "../static/img/n.png", "../static/img/p.png"],
  },
];

let anionFamilies = [
  {
    Name: "[N-]",
    Values: ["[N-]"],
    Labels: [""],
    Imgs: ["../static/img/[n-].png"],
  },
  {
    Name: "[MLn]",
    Values: ["mln"],
    Labels: [""],
    Imgs: ["../static/img/mln.png"],
  },
  {
    Name: "[O-]",
    Values: ["[O-]"],
    Labels: [""],
    Imgs: ["../static/img/[o-].png"],
  },
  {
    Name: "[Cyc]",
    Values: ["cyc"],
    Labels: [""],
    Imgs: ["../static/img/cyc.png"],
  },
  {
    Name: "[Oph]",
    Values: ["oph"],
    Labels: [""],
    Imgs: ["../static/img/oph.png"],
  },
];

var cfamSection = document.querySelector("#select-cfams .box-option-list");
addFamilyContents(cfamSection, cationFamilies);

var afamSection = document.querySelector("#select-afams .box-option-list");
addFamilyContents(afamSection, anionFamilies);

function addFamilyContents(element, content) {
  let allOptionListHTML = "";
  for (var i = 0; i < content.length; i++) {
    // Add parents
    const optionList = content[i];
    let optionListHTML = '<div class="option-list">\n';
    optionListHTML += `\t<h4> ${optionList.Name}</h4>\n`;

    // Add options
    for (let j = 0; j < optionList.Labels.length; j++) {
      const optionLabel = optionList.Labels[j];
      const optionImg = optionList.Imgs[j];
      const optionValue = optionList.Values[j];

      const optionHTML = `\t<div class="option" value=${optionValue}>
                    <img src=${optionImg}></img>
                    <p>${optionLabel}</p></div>\n`;

      optionListHTML += optionHTML;
    }
    optionListHTML += "\n</div>";
    allOptionListHTML += optionListHTML;
  }
  element.innerHTML = allOptionListHTML;
}
