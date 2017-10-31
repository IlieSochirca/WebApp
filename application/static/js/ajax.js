//THE CODE WHICH IS PERFORMING THE AJAX GET REQUEST
//the post like request

$(document).ready(function () {
    var button_post = $('#group-post li button#post-likes');
    button_post.click(function () {
        var postid = $(this).attr("data-postid");  /*when this button is clicked, postid is extracted from this element and then with this postid is made a get request to post-like function. It is successful, a like is added and updated info is returned on our html page(data is the information which is updated in our function)*/
        $.get('/post-like/', {post_pk:postid}, function (data) {
            $("button[data-postid="+postid+"] strong").html(data);
    });
    });
});


//the comment like request

$(document).ready(function () {
    var button_comment = $('#post-comment li button#comment-likes');
    button_comment.click(function () {
        var commentid = $(this).attr("data-commentid");
        $.get('/comment-like/', {comment_pk:commentid}, function (data) {    //in this moment we are sending a request to the server with the comment_id to get the comment object from DB and the view will update it//
            $("button[data-commentid="+commentid+"] strong").html(data);
        });
    });
});
