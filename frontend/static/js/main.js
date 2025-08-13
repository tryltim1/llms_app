
class ScriptScopeApp {
    constructor() {
        this.init();
    }

    init() {
        this.initEventListeners();
        this.initFormHandlers();
        this.initTabHandlers();
        this.initAdminModalHandlers();
        this.initQuillEditor();
    }

    initQuillEditor() {
        // Initialize Quill editor for section content if the element exists
        const createContentElement = document.getElementById('createSectionContent');
        const editContentElement = document.getElementById('editSectionContent');
        
        if (createContentElement) {
            this.createQuillEditor = new Quill('#createSectionContent', {
                theme: 'snow',
                modules: {
                    toolbar: [
                        ['bold', 'italic', 'underline', 'strike'],
                        ['blockquote', 'code-block'],
                        [{ 'header': 1 }, { 'header': 2 }],
                        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                        [{ 'script': 'sub'}, { 'script': 'super' }],
                        [{ 'indent': '-1'}, { 'indent': '+1' }],
                        [{ 'direction': 'rtl' }],
                        [{ 'size': ['small', false, 'large', 'huge'] }],
                        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                        [{ 'color': [] }, { 'background': [] }],
                        [{ 'font': [] }],
                        [{ 'align': [] }],
                        ['clean'],
                        ['link', 'image']
                    ]
                }
            });
        }
        
        if (editContentElement) {
            this.editQuillEditor = new Quill('#editSectionContent', {
                theme: 'snow',
                modules: {
                    toolbar: [
                        ['bold', 'italic', 'underline', 'strike'],
                        ['blockquote', 'code-block'],
                        [{ 'header': 1 }, { 'header': 2 }],
                        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                        [{ 'script': 'sub'}, { 'script': 'super' }],
                        [{ 'indent': '-1'}, { 'indent': '+1' }],
                        [{ 'direction': 'rtl' }],
                        [{ 'size': ['small', false, 'large', 'huge'] }],
                        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                        [{ 'color': [] }, { 'background': [] }],
                        [{ 'font': [] }],
                        [{ 'align': [] }],
                        ['clean'],
                        ['link', 'image']
                    ]
                }
            });
        }
    }

    initEventListeners() {
        // Search functionality
        const searchForm = document.getElementById('searchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleSearch();
            });
        }

        // Sort functionality
        const sortSelect = document.getElementById('sortSelect');
        if (sortSelect) {
            sortSelect.addEventListener('change', () => {
                this.handleSort();
            });
        }
    }

    initAdminModalHandlers() {
        // Create chapter
        const createChapterBtn = document.getElementById('createChapterBtn');
        if (createChapterBtn) {
            createChapterBtn.addEventListener('click', () => {
                this.openModal('createChapterModal');
            });
        }

        // Edit chapter
        const editChapterBtn = document.getElementById('editChapterBtn');
        if (editChapterBtn) {
            editChapterBtn.addEventListener('click', () => {
                this.loadChaptersForEdit();
                this.openModal('editChapterModal');
            });
        }

        // Delete chapter
        const deleteChapterBtn = document.getElementById('deleteChapterBtn');
        if (deleteChapterBtn) {
            deleteChapterBtn.addEventListener('click', () => {
                this.loadChaptersForDelete();
                this.openModal('deleteChapterModal');
            });
        }

        // Section handlers
        this.initSectionModalHandlers();
    }

    initSectionModalHandlers() {
        // Create section
        const createSectionBtn = document.getElementById('createSectionBtn');
        if (createSectionBtn) {
            createSectionBtn.addEventListener('click', () => {
                this.loadChaptersForSection();
                this.openModal('createSectionModal');
            });
        }

        // Edit section
        const editSectionBtn = document.getElementById('editSectionBtn');
        if (editSectionBtn) {
            editSectionBtn.addEventListener('click', () => {
                this.loadChaptersForSection();
                this.openModal('editSectionModal');
            });
        }

        // Delete section
        const deleteSectionBtn = document.getElementById('deleteSectionBtn');
        if (deleteSectionBtn) {
            deleteSectionBtn.addEventListener('click', () => {
                this.loadChaptersForSection();
                this.openModal('deleteSectionModal');
            });
        }

        // Section chapter select change handlers
        const sectionChapterSelects = document.querySelectorAll('.section-chapter-select');
        sectionChapterSelects.forEach(select => {
            select.addEventListener('change', (e) => {
                const chapterId = e.target.value;
                const sectionSelectId = e.target.getAttribute('data-section-select');
                if (chapterId && sectionSelectId) {
                    this.loadSectionsForChapter(chapterId, sectionSelectId);
                }
            });
        });

        // Section select change handler for edit form
        const editSectionSelect = document.getElementById('editSectionSelect');
        if (editSectionSelect) {
            editSectionSelect.addEventListener('change', (e) => {
                const sectionId = e.target.value;
                if (sectionId) {
                    this.loadSectionData(sectionId);
                }
            });
        }
    }

    // Form Handlers
    initFormHandlers() {
        // Comment form
        const addCommentForm = document.getElementById('addCommentForm');
        if (addCommentForm) {
            addCommentForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitComment(e);
            });
        }

        // Admin forms
        this.initAdminFormHandlers();
    }

    initAdminFormHandlers() {
        // Chapter forms
        const createChapterForm = document.getElementById('createChapterForm');
        if (createChapterForm) {
            createChapterForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.createChapter(e);
            });
        }

        const editChapterForm = document.getElementById('editChapterForm');
        if (editChapterForm) {
            editChapterForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.updateChapter(e);
            });
        }

        // Section forms
        const createSectionForm = document.getElementById('createSectionForm');
        if (createSectionForm) {
            createSectionForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.createSection(e);
            });
        }

        const editSectionForm = document.getElementById('editSectionForm');
        if (editSectionForm) {
            editSectionForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.updateSection(e);
            });
        }
    }

    // Tab Handlers
    initTabHandlers() {
        const tabBtns = document.querySelectorAll('[data-tab]');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const tabName = e.target.getAttribute('data-tab');
                this.switchTab(tabName);
            });
        });
    }

    switchTab(tabName) {
        // Hide all tab contents
        const tabContents = document.querySelectorAll('.admin-tab-content');
        tabContents.forEach(content => {
            content.classList.add('d-none');
        });

        // Remove active class from all buttons
        const tabBtns = document.querySelectorAll('.admin-tab-btn');
        tabBtns.forEach(btn => {
            btn.classList.remove('active');
        });

        // Show selected tab
        const selectedTab = document.getElementById(tabName + 'Tab');
        if (selectedTab) {
            selectedTab.classList.remove('d-none');
        }

        // Add active class to selected button
        const selectedBtn = document.querySelector(`[data-tab="${tabName}"]`);
        if (selectedBtn) {
            selectedBtn.classList.add('active');
        }
    }

    // Modal functions
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            const bsModal = new bootstrap.Modal(modal, {
                backdrop: 'static',
                keyboard: true
            });

            // Ensure modal is centered when shown
            modal.addEventListener('shown.bs.modal', () => {
                this.centerModal(modal);
            }, { once: true });

            bsModal.show();
        }
    }

    centerModal(modal) {
        const modalDialog = modal.querySelector('.modal-dialog');
        if (modalDialog) {
            const top = Math.max(0, (window.innerHeight - modalDialog.clientHeight) / 2);
            modalDialog.style.marginTop = `${top}px`;
        }
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) {
                bootstrapModal.hide();
            }
        }
    }

    // Load data functions
    async loadChaptersForEdit() {
        try {
            const response = await fetch('/api/admin/chapters');
            const chapters = await response.json();
            const select = document.getElementById('editChapterSelect');
            
            if (select) {
                select.innerHTML = '<option value="">Choose a chapter to edit...</option>';
                chapters.forEach(chapter => {
                    const option = document.createElement('option');
                    option.value = chapter.id;
                    option.textContent = chapter.name;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            this.showToast('Failed to load chapters', 'error');
            console.error('Error loading chapters:', error);
        }
    }

    async loadChaptersForDelete() {
        try {
            const response = await fetch('/api/admin/chapters');
            const chapters = await response.json();
            const select = document.getElementById('deleteChapterSelect');
            
            if (select) {
                select.innerHTML = '<option value="">Choose a chapter to delete...</option>';
                chapters.forEach(chapter => {
                    const option = document.createElement('option');
                    option.value = chapter.id;
                    option.textContent = chapter.name;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            this.showToast('Failed to load chapters', 'error');
            console.error('Error loading chapters:', error);
        }
    }

    async loadChaptersForSection() {
        try {
            const response = await fetch('/api/admin/chapters');
            const chapters = await response.json();
            
            // Load for create section modal
            const createSelect = document.getElementById('createSectionChapterSelect');
            if (createSelect) {
                createSelect.innerHTML = '<option value="">Choose a chapter...</option>';
                chapters.forEach(chapter => {
                    const option = document.createElement('option');
                    option.value = chapter.id;
                    option.textContent = chapter.name;
                    createSelect.appendChild(option);
                });
            }

            // Load for edit section modal
            const editSelect = document.getElementById('editSectionChapterSelect');
            if (editSelect) {
                editSelect.innerHTML = '<option value="">Choose a chapter...</option>';
                chapters.forEach(chapter => {
                    const option = document.createElement('option');
                    option.value = chapter.id;
                    option.textContent = chapter.name;
                    editSelect.appendChild(option);
                });
            }

            // Load for delete section modal
            const deleteSelect = document.getElementById('deleteSectionChapterSelect');
            if (deleteSelect) {
                deleteSelect.innerHTML = '<option value="">Choose a chapter...</option>';
                chapters.forEach(chapter => {
                    const option = document.createElement('option');
                    option.value = chapter.id;
                    option.textContent = chapter.name;
                    deleteSelect.appendChild(option);
                });
            }
        } catch (error) {
            this.showToast('Failed to load chapters', 'error');
            console.error('Error loading chapters:', error);
        }
    }

    async loadSectionsForChapter(chapterId, sectionSelectId) {
        try {
            const response = await fetch(`/api/admin/sections/${chapterId}`);
            const sections = await response.json();
            const select = document.getElementById(sectionSelectId);
            
            if (select) {
                select.innerHTML = '<option value="">Choose a section...</option>';
                sections.forEach(section => {
                    const option = document.createElement('option');
                    option.value = section.id;
                    option.textContent = section.name;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            this.showToast('Failed to load sections', 'error');
            console.error('Error loading sections:', error);
        }
    }

    async loadSectionData(sectionId) {
        try {
            const chapterId = document.getElementById('editSectionChapterSelect').value;
            const response = await fetch(`/api/admin/sections/${chapterId}`);
            const sections = await response.json();
            
            const section = sections.find(s => s.id == sectionId);
            if (section) {
                const nameInput = document.getElementById('editSectionName');
                if (nameInput) nameInput.value = section.name;
                
                if (this.editQuillEditor) {
                    this.editQuillEditor.root.innerHTML = section.content || '';
                }
            }
        } catch (error) {
            this.showToast('Failed to load section data', 'error');
            console.error('Error loading section data:', error);
        }
    }

    // CRUD Operations
    async createChapter(e) {
        const formData = new FormData(e.target);
        const data = {
            name: formData.get('name')
        };

        try {
            const response = await fetch('/api/chapters', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                this.showToast('Chapter created successfully!', 'success');
                this.closeModal('createChapterModal');
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showToast(result.message || 'Failed to create chapter', 'error');
            }
        } catch (error) {
            this.showToast('Error creating chapter', 'error');
            console.error('Error creating chapter:', error);
        }
    }

    async updateChapter(e) {
        const formData = new FormData(e.target);
        const chapterId = formData.get('chapter_id');
        const data = {
            name: formData.get('name')
        };

        if (!chapterId) {
            this.showToast('Please select a chapter to edit', 'error');
            return;
        }

        try {
            const response = await fetch(`/api/chapters/${chapterId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                this.showToast('Chapter updated successfully!', 'success');
                this.closeModal('editChapterModal');
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showToast(result.message || 'Failed to update chapter', 'error');
            }
        } catch (error) {
            this.showToast('Error updating chapter', 'error');
            console.error('Error updating chapter:', error);
        }
    }

    async createSection(e) {
        const formData = new FormData(e.target);
        const content = this.createQuillEditor ? this.createQuillEditor.root.innerHTML : formData.get('content');
        
        const data = {
            chapter_id: formData.get('chapter_id'),
            name: formData.get('name'),
            content: content
        };

        try {
            const response = await fetch('/api/sections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                this.showToast('Section created successfully!', 'success');
                this.closeModal('createSectionModal');
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showToast(result.message || 'Failed to create section', 'error');
            }
        } catch (error) {
            this.showToast('Error creating section', 'error');
            console.error('Error creating section:', error);
        }
    }

    async updateSection(e) {
        const formData = new FormData(e.target);
        const sectionId = formData.get('section_id');
        const content = this.editQuillEditor ? this.editQuillEditor.root.innerHTML : formData.get('content');
        
        const data = {
            name: formData.get('name'),
            content: content
        };

        if (!sectionId) {
            this.showToast('Please select a section to edit', 'error');
            return;
        }

        try {
            const response = await fetch(`/api/sections/${sectionId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                this.showToast('Section updated successfully!', 'success');
                this.closeModal('editSectionModal');
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showToast(result.message || 'Failed to update section', 'error');
            }
        } catch (error) {
            this.showToast('Error updating section', 'error');
            console.error('Error updating section:', error);
        }
    }

    async deleteChapter(chapterId) {
        try {
            const response = await fetch(`/api/chapters/${chapterId}`, {
                method: 'DELETE'
            });

            const result = await response.json();
            
            if (result.success) {
                this.showToast('Chapter deleted successfully!', 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showToast(result.message || 'Failed to delete chapter', 'error');
            }
        } catch (error) {
            this.showToast('Error deleting chapter', 'error');
            console.error('Error deleting chapter:', error);
        }
    }

    async deleteSection(sectionId) {
        try {
            const response = await fetch(`/api/sections/${sectionId}`, {
                method: 'DELETE'
            });

            const result = await response.json();
            
            if (result.success) {
                this.showToast('Section deleted successfully!', 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showToast(result.message || 'Failed to delete section', 'error');
            }
        } catch (error) {
            this.showToast('Error deleting section', 'error');
            console.error('Error deleting section:', error);
        }
    }

    // Comment functionality
    async submitComment(e) {
        const form = e.target;
        const formData = new FormData(form);
        
        const data = {
            content: formData.get('content'),
            chapter_id: formData.get('chapter_id') || null,
            section_id: formData.get('section_id') || null
        };

        try {
            const response = await fetch('/api/comments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                this.showToast('Comment added successfully!', 'success');
                form.reset();
                // Reload comments
                if (data.chapter_id) {
                    this.loadChapterComments(data.chapter_id);
                } else if (data.section_id) {
                    this.loadSectionComments(data.section_id);
                }
            } else {
                this.showToast(result.message || 'Failed to add comment', 'error');
            }
        } catch (error) {
            this.showToast('Error adding comment', 'error');
            console.error('Error adding comment:', error);
        }
    }

    // Search and sort functions
    handleSearch() {
        const form = document.getElementById('searchForm');
        if (form) {
            form.submit();
        }
    }

    handleSort() {
        const form = document.getElementById('searchForm');
        if (form) {
            form.submit();
        }
    }

    // Utility functions
    showToast(message, type = 'info') {
        // Create toast container if it doesn't exist
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '1055';
            document.body.appendChild(toastContainer);
        }

        // Create toast
        const toastId = 'toast-' + Date.now();
        const toast = document.createElement('div');
        toast.id = toastId;
        toast.className = `toast align-items-center text-bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'primary'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        toastContainer.appendChild(toast);

        // Show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
}

// Global functions for template usage
function showConfirmDelete(type, id, name) {
    const modal = document.getElementById('confirmDeleteModal');
    const modalBody = modal.querySelector('.modal-body');
    const confirmBtn = document.getElementById('confirmDeleteActionBtn');
    
    modalBody.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>
            Are you sure you want to delete the ${type} <strong>"${name}"</strong>?
            ${type === 'chapter' ? '<br><small>This will also delete all sections within this chapter.</small>' : ''}
        </div>
        <p class="text-muted">This action cannot be undone.</p>
    `;
    
    confirmBtn.onclick = () => {
        if (type === 'chapter') {
            window.scriptScopeApp.deleteChapter(id);
        } else if (type === 'section') {
            window.scriptScopeApp.deleteSection(id);
        }
        bootstrap.Modal.getInstance(modal).hide();
    };
    
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    window.scriptScopeApp = new ScriptScopeApp();
});
