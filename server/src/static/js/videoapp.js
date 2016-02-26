/**
 * Created by server on 16-1-7.
 */
jQuery(function(){
        $('.ctrlPanel').find("span").each(
            function(){
            $(this).hover(
                function(){
                    $(this).addClass("sel");
                    },
                function(){
                    $(this).removeClass();
                    }
                    )
                  });
    }
);