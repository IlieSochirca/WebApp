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


$(document).ready(function (e) {
    var follow_button = $("#followers-group button#followers-click");
    var user = $('.username').data('value');
    follow_button.click(function () {
       var groupid = $(this).attr('data-groupid');
       if ($("div#followers-group p").filter(":contains('"+user+"')").length==0) {
           // console.log('bbbbb');
           // console.log($("div#followers-group p").filter(":contains('" + user + "')"));
           $.get('/group-follow/', {group_pk: groupid}, function (data) {
               // console.log('ssss');
               $("div h5 strong#group_follow_count").html(data);
               $("#followers-group ").append('<p><a href="/userprofile/'+user+'">' + user + '</a></p>');
               console.log(user)
               $(follow_button).html('Unfollow');
               console.log('add')
               // console.log(data);
               // console.log(user);
           });
       } else {
           $.get('/group-follow/', {group_pk: groupid}, function (data) {
                $("div h5 strong#group_follow_count").html(data);
                // alert("Do you really want to unfollow this group?");
                $("div p").filter(":contains('"+user+"')").remove();
                $(follow_button).html('Follow');
                console.log('remove')
           })
           }
       });
});

$(document).ready(function () {
    $('#add_id_category').click(function (data) {
        $('#select_list').autocomplete()
    })

})