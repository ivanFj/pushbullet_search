var baseFormContent = "<div class='mdl-textfield mdl-js-textfield mdl-textfield--floating-label'>\
						<input class='mdl-textfield__input' type='text' id='title'>\
						<label class='mdl-textfield__label' for='title'>Title...</label>\
					</div>\
					<div class='mdl-textfield mdl-js-textfield mdl-textfield--floating-label'>\
						<textarea class='mdl-textfield__input' type='text' rows= '3' id='body' ></textarea>\
						<label class='mdl-textfield__label' for='body'>Body...</label>\
					</div>\
					<div class='mdl-textfield mdl-js-textfield mdl-textfield--floating-label'>\
						<input class='mdl-textfield__input' type='text' id='url'>\
						<label class='mdl-textfield__label' for='url'>Url...</label>\
					</div>";
					
var formButtons = "<div class='mdl-card__actions'>\
						<button class='mdl-button mdl-js-button mdl-button--raised mdl-button--accent mdl-js-ripple-effect submit'>\
							<i class='material-icons'>done</i><span class='icon-text'> Submit</span>\
						</button>\
						<button class='mdl-button mdl-js-button mdl-button--raised mdl-button--accent mdl-js-ripple-effect cancel'>\
							<i class='material-icons'>cancel</i><span class='icon-text'> Cancel</span>\
						</button>\
					</div>";
						
var actionsDiv = document.querySelector(".pushes .mdl-card__actions").cloneNode(true).outerHTML;
var pushes = document.getElementsByClassName("pushes");
var snackbarContainer = document.getElementById('toast');
var accessToken = {"Access-Token" : "o.tYINVKNMCABJX6Icag5ldJ2X6p7KyMog"};
			
function getResponse(url, initData){
	
	var data = {message : "Default message"}
	
	return fetch(url, initData).then(function(response){
	
		if (response.ok){
			
			data.message = initData.method.toLowerCase() === "delete"  ? "The push was deleted" : "The push was updated";
			
		}else{
			
			if (response.headers.get("content-type").indexOf("application/json") >= 0){
			
				if (response.status === 404){
					
					data.message = initData.method.toLowerCase() === "delete"  ? "The push was deleted" 
									: "The requested item does not exist";
					
				}else{
				
					return response.json().then(function(json){
						data.message = "There was a problem with this push: " + json['error']['message'] ;
						return Promise.reject(data.message);
					});
			
				}
			
			}else{
				
				return Promise.reject("The push could not be deleted: " + response.status);
				
			}
			
		}
		
		snackbarContainer.MaterialSnackbar.showSnackbar(data);
		return response	
		
	}).catch(function(error){
		
		
		if (error.message){
			data.message = "There was a problem with the fetch request: " + error.message;
		}else{
			data.message = error
		}
		
		snackbarContainer.MaterialSnackbar.showSnackbar(data);
		return Promise.reject();
		
	});
	
}

for (var i = 0; i < pushes.length; i++){
	
	var pushElement = pushes[i];
	
	pushElement.addEventListener("transitionend", function(event){
		if (event.target && event.target.matches("div.delete-push")){
			this.remove();
		}else if(event.target && event.target.matches("div.transition-grow")){
			var dimensions = this.getBoundingClientRect();
			this.style.minHeight = dimensions.height + "px";
		}else if(event.target && event.target.matches("div.fade-div")){
			this.querySelector(".fade-div").style.zIndex = "";
		}
	}, true);
	
	pushElement.onclick = function(event){
		
		var targetElement = event.target.parentElement;
		
		if (targetElement){
		
			var containerDiv = this;
			var iden = containerDiv.getAttribute("data-iden");
			
			if (targetElement.matches("button.change")){
				
				var fadeDiv = containerDiv.querySelector(".fade-div");
				fadeDiv.classList.remove("fade-in");
				fadeDiv.style.zIndex = "9999";
				
				var loadingSpinner = containerDiv.querySelector(".loading");
				var dimensions = containerDiv.getBoundingClientRect();
				containerDiv.style.minHeight = dimensions.height;
				
				var openedForm = document.getElementById("update-form");
				
				if (openedForm){
					
					openedForm.nextElementSibling.querySelector(".cancel").lastChild.click();
					
				}
				
				containerDiv.classList.add("transition-grow");
				
				var instanceForm = baseFormContent;
				var formElement = document.createElement("form");
				var titleElement = containerDiv.querySelector(".title");
				var titleValue = titleElement ? titleElement.textContent : "";
				var bodyElement = containerDiv.querySelector(".body");
				var bodyValue = bodyElement ? bodyElement.textContent : "";
				var urlElement = containerDiv.querySelector(".url");
				var urlValue = urlElement ? urlElement.textContent : "";
				
				formElement.setAttribute("id", "update-form");
				formElement.insertAdjacentHTML("beforeend", instanceForm);
				formElement.querySelector("#title").value = titleValue;
				formElement.querySelector("#body").value = bodyValue;
				formElement.querySelector("#url").value = urlValue;

				this.containerClone = containerDiv.cloneNode(true);
				this.containerClone.lastElementChild.remove();
				
				componentHandler.upgradeElements(formElement.getElementsByClassName("mdl-textfield"));
				containerDiv.innerHTML = "";
				containerDiv.appendChild(loadingSpinner);
				containerDiv.appendChild(fadeDiv);
				containerDiv.appendChild(formElement);
				containerDiv.insertAdjacentHTML("beforeend", formButtons);
				componentHandler.upgradeElements(containerDiv.querySelectorAll(".mdl-button"));
				window.getComputedStyle(containerDiv.querySelector(".fade-div")).opacity;
				containerDiv.querySelector(".fade-div").classList.add("fade-in");
				
			}else if (targetElement.matches("button.delete")){

				var initData = {headers : accessToken, method : "delete"};
				var currentElement = this;
				var loadingSpinner = currentElement.querySelector(".loading");
				loadingSpinner.classList.remove("hide");
				loadingSpinner.querySelector(".loading-text").classList.add("delete-text");
				
				getResponse("https://api.pushbullet.com/v2/pushes" + "/" + iden, initData).then(function(response){
					
					currentElement.classList.add("delete-push");
					
				}).catch(function(event){
					
					loadingSpinner.classList.add("hide");
					
				});
				
			}else if (targetElement.matches("button.submit")){
				
				var containerClone = this.containerClone;
				
				var data = {device_iden : "ujz4IpIwmKisjAiVsKnSTs", type : 'link', url : document.getElementById("url").value, 
							body : document.getElementById("body").value || "", title : document.getElementById("title").value || ""};
				accessToken["content-type"] = "application/json";
				var postData = {headers : accessToken, body : JSON.stringify(data), method : "post"};
				var deleteData = {headers : accessToken, method : 'delete'};
				var message = "Default message";
				
				var loadingSpinner = containerDiv.querySelector(".loading");
				loadingSpinner.classList.remove("hide");
				loadingSpinner.querySelector(".loading-text").classList.add("update-text");
				
				getResponse("https://api.pushbullet.com/v2/pushes" + "/" + iden, deleteData).then(function(response){
						
					getResponse("https://api.pushbullet.com/v2/pushes", postData).then(function(httpResponse){
						
						if (httpResponse.ok){
							
							return httpResponse.json();
							
						}
						
					}).then(function(data){
							
						var iden =  data.iden;
						var title = data.title || "";
						var body = data.body || "";
						var url = data.url || "";
						
						var titleHtmlString = "";
						var bodyHtmlString = "";
						var urlHtmlString = "";
						
						var loadingSpinner = containerDiv.querySelector(".loading");
						
						containerDiv.classList.remove("transition-grow");
						containerDiv.style.minHeight = "";
						
						if (title){
							
							var titleElement = containerClone.querySelector(".title");
							
							if (!titleElement){								
								titleElement = document.createElement("h5");
								titleElement.className = "title";
							}
							
							titleElement.textContent = title;
							titleHtmlString = titleElement.outerHTML;
							
						}
						if (body){
							
							var bodyElement = containerClone.querySelector(".body");
							
							if (!bodyElement){
								bodyElement = document.createElement("p");
								bodyElement.className = "body";
							}
							
							bodyElement.textContent = body;
							bodyHtmlString = bodyElement.outerHTML;
							
						}
						if (url){
							
							var urlElement = containerClone.querySelector(".url");
							
							if (!urlElement){
								urlElement = document.createElement("a");
								urlElement.className = "url";
							}
							
							urlElement.setAttribute("href", url);
							urlElement.textContent = url;
							urlHtmlString = urlElement.outerHTML;
							
						}
						
						containerDiv.querySelector(".loading").classList.add("hide");
						
						containerDiv.setAttribute("data-iden", iden);
						containerDiv.innerHTML = "";
						containerDiv.appendChild(loadingSpinner);
						containerDiv.insertAdjacentHTML("beforeend",containerClone.querySelector(".fade-div").outerHTML);
						containerDiv.insertAdjacentHTML("beforeend", titleHtmlString + bodyHtmlString + urlHtmlString);
						containerDiv.insertAdjacentHTML("beforeend", actionsDiv);
						componentHandler.upgradeElements(containerDiv.querySelectorAll("button"));
						window.getComputedStyle(containerDiv.querySelector(".fade-div")).opacity;
						containerDiv.querySelector(".fade-div").classList.add("fade-in");
						
					}).catch(function(){
						
						containerDiv.querySelector(".loading").classList.add("hide");
						
					});
					
				}).catch(function(){
					
					containerDiv.querySelector(".loading").classList.add("hide");
					
				});
				
			}else if (targetElement.matches("button.cancel")){
				
				containerDiv.classList.remove("transition-grow");
				containerDiv.style.minHeight = "";
				
				
				containerDiv.innerHTML = '';
				containerDiv.insertAdjacentHTML("beforeend", this.containerClone.innerHTML);
				containerDiv.insertAdjacentHTML("beforeend", actionsDiv);
				componentHandler.upgradeElements(containerDiv.querySelectorAll("button"));
				
				window.getComputedStyle(containerDiv.querySelector(".fade-div")).opacity;
				containerDiv.querySelector(".fade-div").classList.add("fade-in");
				
			}
			
		}
		
	};
	
}