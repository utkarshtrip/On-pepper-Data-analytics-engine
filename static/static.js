document.addEventListener('DOMContentLoaded', function () {
    const dragColumn = document.getElementById('dragColumn');
    const targetIframe = document.getElementById('targetIframe');

    dragColumn.addEventListener('dragstart', function(event){
        event.dataTransfer.setData( 'text/plain', event.target.id);
    });

    targetIframe.addEventListener('load', function(){
        const iframeWindow = targetIframe.contentWindow;

        window.addEventListener('message', function(event){
            if (event.source === iframeWindow && event.data === 'readyForDrop'){
                iframeWindow.postMessage({type: 'allowDrop'}, '*');
            }
        });

        iframeWindow.postMessage({type: 'mainWindowReady'}, '*');
    });
});