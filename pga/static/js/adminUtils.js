
/* Used to create upload dialogs for admin pages 
    fileUploadId is the id of the input DOM element to be used for uploading
    uploadCallback should contain the logic for submitting form along with 
        any other associated data
*/
function createUploadDialog(fileUploadId, uploadCallback) {
    
    var actualUploadCallback = uploadCallback;
    
    //Creates default callback that simply submits form without extra data
    if(!actualUploadCallback){
        actualUploadCallback = function() {
            $("#uploadForm").submit();
        };
    }
    
    var uploadDialog = $("#uploadDialog").dialog({
      autoOpen: false,
      height: 400,
      width: 450,
      modal: true,
      buttons: [
        {
            id: "cancel",
            text: "Cancel",
            click: function() { uploadDialog.dialog("close"); }
        },
        {
            id: "uploadBtn",
            text: "Upload",
            disabled: 'true',
            click: actualUploadCallback
        }
      ],
      Close: function() {
        
      }
    });

    var handleFiles = function() {
		var disabled = document.getElementById(fileUploadId).files.length == 0;
		$("#uploadBtn").button("option", "disabled", disabled);
	};
    
    var inputElement = document.getElementById(fileUploadId);
    inputElement.addEventListener("change", handleFiles, false);
    
    return uploadDialog;
}

function createConfirmDeleteDialog(confirmDeleteCallback){
    var confirmDeleteDialog = $("#confirmDeleteDialog").dialog({
      autoOpen: false,
      height: 400,
      width: 450,
      modal: true,
      buttons: [
        {
            id: "deleteBtn",
            text: "Delete",
            click: confirmDeleteCallback
        },
        {
            id: "cancel",
            text: "Cancel",
            click: function() { confirmDeleteDialog.dialog("close"); }
        }
      ],
      Close: function() {
        
      }
    });
    
    return confirmDeleteDialog;
}

function initEditButton() {
    $("#editBtn").click(function() {
        editing = !editing;
        $(".removeBtn").toggle();
        if(editing){
            $(this).text('Stop Editing');
        }
        else {
            $(this).text('Edit');
        }
    });
}