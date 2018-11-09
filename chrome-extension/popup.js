// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

//let send = document.getElementById("send");
let note = document.getElementById("note");
let notes = document.getElementById("notes");

function sendPost(data){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function(){
            if (xhr.readyState == XMLHttpRequest.DONE){
                notes.value = xhr.responseText;
            }
        }
        xhr.open("POST", "http://localhost:9999", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({"url":tabs[0].url, "note":data}));
    });
}

sendPost("");

/*
send.onclick = function(){
    sendPost(note.value);
    note.value = "";
};
*/

note.addEventListener("keyup", function(event){
    event.preventDefault();
    if (event.keyCode === 13){
        //send.click();
        sendPost(note.value);
        note.value = "";
    }
});
