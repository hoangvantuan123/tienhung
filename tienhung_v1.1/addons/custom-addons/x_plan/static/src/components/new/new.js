/** @odoo-module */

const { Component, onWillStart, useState } = owl;

export class New extends Component {
    setup() {
        this.pageSize = 3; // Số lượng bài viết hiển thị trên mỗi trang
        this.state = useState({
            data_post: [
                { id: 1, title: "Bài viết 1", content: "Nội dung bài viết 1", date: "2024-07-01", time: "12:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" },
                { id: 2, title: "Bài viết 2", content: "Nội dung bài viết 2", date: "2024-07-02", time: "14:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" },
                { id: 3, title: "Bài viết 3", content: "Nội dung bài viết 3", date: "2024-07-03", time: "16:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8fHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" },
                { id: 4, title: "Bài viết 4", content: "Nội dung bài viết 4", date: "2024-07-04", time: "18:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8fHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" },
                { id: 5, title: "Bài viết 5", content: "Nội dung bài viết 5", date: "2024-07-05", time: "20:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8fHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" },
                { id: 6, title: "Bài viết 6", content: "Nội dung bài viết 6", date: "2024-07-06", time: "22:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8fHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" },
                { id: 7, title: "Bài viết 7", content: "Nội dung bài viết 7", date: "2024-07-07", time: "00:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8fHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" },
                { id: 8, title: "Bài viết 8", content: "Nội dung bài viết 8", date: "2024-07-08", time: "02:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8fHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" },
                { id: 9, title: "Bài viết 9", content: "Nội dung bài viết 9", date: "2024-07-09", time: "04:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8fHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" },
                { id: 10, title: "Bài viết 10", content: "Nội dung bài viết 10", date: "2024-07-10", time: "06:00", imageUrl: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDF8fHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" }
            ],
            currentPage: 1,
            selectedPost: null,
            showNew: false
        });

        onWillStart(async () => {
            this.handlePostClick = this.handlePostClick.bind(this);
            this.closeModelNew = this.closeModelNew.bind(this);
        });
    }

    get paginatedPosts() {
        const startIndex = (this.state.currentPage - 1) * this.pageSize;
        const endIndex = startIndex + this.pageSize;
        return this.state.data_post.slice(startIndex, endIndex);
    }

    nextPage() {
        if (this.state.currentPage * this.pageSize< this.state.data_post.length) {
            this.state.currentPage += 1;
        }
    }

    prevPage() {
        if (this.state.currentPage > 1) {
            this.state.currentPage -= 1;
        }
    }
    closeModelNew() {
        this.state.showNew = false;
        this.state.selectedPost = null;
    }
    handlePostClick(ev, post = null) {
        if (post) {
            this.state.showNew = !this.state.showNew;
            this.state.selectedPost = post;
            console.log('ID bài viết được chọn:', post);
        } else {
            console.log('No post selected or post parameter is null.');
        }
    }
}

New.template = "owl.New";
