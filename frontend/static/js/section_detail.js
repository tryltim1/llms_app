// JS for section_detail.html

document.addEventListener('DOMContentLoaded', function() {
    const commentContent = document.getElementById('commentContent');
    if (commentContent) {
        commentContent.removeAttribute('disabled');
        commentContent.value = '';
    }

    const addCommentModal = document.getElementById('addCommentModal');
    addCommentModal.addEventListener('show.bs.modal', function (event) {
        if (commentContent) {
            commentContent.value = '';
            commentContent.focus();
        }
        const form = document.getElementById('addCommentForm');
        form.removeAttribute('data-section-id');
        const button = event.relatedTarget;
        if (button && button.hasAttribute('data-section-id')) {
            form.setAttribute('data-section-id', button.getAttribute('data-section-id'));
        }
    });

    const addCommentForm = document.getElementById('addCommentForm');
    addCommentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const content = commentContent.value.trim();
        if (!content) {
            alert('Comment cannot be empty.');
            return;
        }
        let endpoint = '';
        let payload = { content: content };
        if (addCommentForm.hasAttribute('data-section-id')) {
            endpoint = '/api/section_comments';
            payload.section_id = addCommentForm.getAttribute('data-section-id');
        } else {
            alert('No target for comment.');
            return;
        }
        fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                var modalInstance = bootstrap.Modal.getOrCreateInstance(addCommentModal);
                modalInstance.hide();
                alert('Comment added successfully!');
                addCommentForm.reset();
            } else {
                alert(data.message || 'Failed to add comment.');
            }
        })
        .catch(() => {
            alert('Error submitting comment.');
        });
    });
});
