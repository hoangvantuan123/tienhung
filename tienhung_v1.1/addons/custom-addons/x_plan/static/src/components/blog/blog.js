/** @odoo-module */

const { Component, onWillStart, useState } = owl;

export class Blog extends Component {
  setup() {
    this.pageSize = 8;
    this.state = useState({
      showSurvey: false,
      data_survey: [
        {
          id: 1,
          title:
            "Khảo Sát Mức Độ Hài Lòng Của Khách Hàng Về Dịch Vụ Chăm Sóc Khách Hàng",
          questions: [
            {
              id: 1,
              question:
                "Bạn đã sử dụng dịch vụ chăm sóc khách hàng của chúng tôi trong khoảng thời gian nào?",
              type: "multiple-choice",
              options: [
                "Trong tháng qua",
                "Trong 3 tháng qua",
                "Trong 6 tháng qua",
                "Hơn 6 tháng",
              ],
            },
            {
              id: 2,
              question:
                "Bạn đánh giá thế nào về thời gian phản hồi của dịch vụ chăm sóc khách hàng?",
              type: "multiple-choice",
              options: [
                "Rất hài lòng",
                "Hài lòng",
                "Trung lập",
                "Không hài lòng",
                "Rất không hài lòng",
              ],
            },
            {
              id: 3,
              question:
                "Đánh giá của bạn về sự chuyên nghiệp và thái độ của nhân viên chăm sóc khách hàng?",
              type: "multiple-choice",
              options: ["Rất tốt", "Tốt", "Trung bình", "Kém", "Rất kém"],
            },
            {
              id: 4,
              question:
                "Bạn có gặp phải bất kỳ vấn đề nào trong quá trình sử dụng dịch vụ không?",
              type: "yes-no",
            },
            {
              id: 4.1,
              question: "Nếu có, vui lòng mô tả vấn đề:",
              type: "text",
              conditional: {
                questionId: 4,
                value: "Có",
              },
            },
            {
              id: 5,
              question:
                "Bạn có đề xuất gì để chúng tôi cải thiện dịch vụ chăm sóc khách hàng không?",
              type: "text",
            },
            {
              id: 6,
              question:
                "Bạn có sẵn sàng giới thiệu dịch vụ của chúng tôi cho bạn bè hoặc người thân không?",
              type: "yes-no",
            },
          ],
          responses: [
            {
              questionId: 1,
              selectedOptions: ["Trong tháng qua"],
            },
            {
              questionId: 2,
              selectedOptions: ["Hài lòng"],
            },
            {
              questionId: 3,
              selectedOptions: ["Tốt"],
            },
            {
              questionId: 4,
              answer: "Có",
              responseDetail: "Đã gặp vấn đề với thời gian phản hồi.",
            },
            {
              questionId: 5,
              answer: "Nên cải thiện thời gian phản hồi và đào tạo nhân viên.",
            },
            {
              questionId: 6,
              answer: "Có",
            },
          ],
        },
        {
          id: 2,
          title: "Khảo Sát Sự Hài Lòng Với Sản Phẩm",
          questions: [
            {
              id: 1,
              question:
                "Bạn đã sử dụng sản phẩm của chúng tôi trong khoảng thời gian nào?",
              type: "multiple-choice",
              options: [
                "Trong tuần qua",
                "Trong tháng qua",
                "Trong 3 tháng qua",
                "Trên 3 tháng",
              ],
            },
            {
              id: 2,
              question: "Bạn đánh giá thế nào về chất lượng của sản phẩm?",
              type: "multiple-choice",
              options: ["Rất tốt", "Tốt", "Trung bình", "Kém", "Rất kém"],
            },
            {
              id: 3,
              question: "Bạn có gặp phải vấn đề gì khi sử dụng sản phẩm không?",
              type: "yes-no",
            },
            {
              id: 3.1,
              question: "Nếu có, vui lòng mô tả vấn đề:",
              type: "text",
              conditional: {
                questionId: 3,
                value: "Có",
              },
            },
            {
              id: 4,
              question:
                "Bạn có đề xuất gì để chúng tôi cải thiện sản phẩm không?",
              type: "text",
            },
          ],
          responses: [
            {
              questionId: 1,
              selectedOptions: ["Trong tháng qua"],
            },
            {
              questionId: 2,
              selectedOptions: ["Tốt"],
            },
            {
              questionId: 3,
              answer: "Có",
              responseDetail:
                "Sản phẩm có hiện tượng hỏng hóc sau một thời gian ngắn sử dụng.",
            },
            {
              questionId: 4,
              answer:
                "Cần cải thiện chất lượng và kiểm tra sản phẩm kỹ hơn trước khi xuất xưởng.",
            },
          ],
        },
        {
          id: 10,
          title: "Khảo Sát Điều Kiện Sống Của Công Nhân",
          questions: [
            {
              id: 1,
              question:
                "Bạn cảm thấy điều kiện sinh hoạt của bạn tại khu vực lưu trú như thế nào?",
              type: "multiple-choice",
              options: ["Rất tốt", "Tốt", "Trung bình", "Kém", "Rất kém"],
            },
            {
              id: 2,
              question:
                "Có đủ tiện nghi và dịch vụ hỗ trợ cần thiết trong khu vực lưu trú của bạn không?",
              type: "multiple-choice",
              options: ["Rất đủ", "Đủ", "Trung bình", "Thiếu", "Rất thiếu"],
            },
            {
              id: 3,
              question:
                "Bạn có gặp phải vấn đề gì liên quan đến an ninh và an toàn trong khu vực lưu trú không?",
              type: "yes-no",
            },
            {
              id: 3.1,
              question: "Nếu có, vui lòng mô tả vấn đề:",
              type: "text",
              conditional: {
                questionId: 3,
                value: "Có",
              },
            },
            {
              id: 4,
              question:
                "Bạn có đề xuất gì để cải thiện điều kiện sinh hoạt không?",
              type: "text",
            },
          ],
          responses: [
            {
              questionId: 1,
              selectedOptions: ["Tốt"],
            },
            {
              questionId: 2,
              selectedOptions: ["Đủ"],
            },
            {
              questionId: 3,
              answer: "Có",
              responseDetail: "Có vấn đề về an ninh vào ban đêm.",
            },
            {
              questionId: 4,
              answer:
                "Cần tăng cường bảo vệ an ninh và cải thiện cơ sở vật chất trong khu vực lưu trú.",
            },
          ],
        },
        {
          id: 11,
          title: "Khảo Sát Môi Trường Làm Việc",
          questions: [
            {
              id: 1,
              question:
                "Bạn đánh giá thế nào về môi trường làm việc hiện tại của bạn?",
              type: "multiple-choice",
              options: ["Rất tốt", "Tốt", "Trung bình", "Kém", "Rất kém"],
            },
            {
              id: 2,
              question:
                "Có đủ trang thiết bị và công cụ cần thiết để bạn hoàn thành công việc không?",
              type: "multiple-choice",
              options: ["Rất đủ", "Đủ", "Trung bình", "Thiếu", "Rất thiếu"],
            },
            {
              id: 3,
              question:
                "Bạn có cảm thấy rằng bạn được hỗ trợ đầy đủ từ quản lý và đồng nghiệp không?",
              type: "multiple-choice",
              options: [
                "Rất đồng ý",
                "Đồng ý",
                "Trung lập",
                "Không đồng ý",
                "Rất không đồng ý",
              ],
            },
            {
              id: 4,
              question:
                "Bạn có gặp khó khăn gì trong việc giao tiếp với quản lý hoặc đồng nghiệp không?",
              type: "yes-no",
            },
            {
              id: 4.1,
              question: "Nếu có, vui lòng mô tả vấn đề:",
              type: "text",
              conditional: {
                questionId: 4,
                value: "Có",
              },
            },
            {
              id: 5,
              question:
                "Bạn có đề xuất gì để cải thiện môi trường làm việc không?",
              type: "text",
            },
          ],
          responses: [
            {
              questionId: 1,
              selectedOptions: ["Tốt"],
            },
            {
              questionId: 2,
              selectedOptions: ["Đủ"],
            },
            {
              questionId: 3,
              selectedOptions: ["Đồng ý"],
            },
            {
              questionId: 4,
              answer: "Có",
              responseDetail:
                "Gặp khó khăn trong việc tiếp cận thông tin từ quản lý.",
            },
            {
              questionId: 5,
              answer:
                "Cần cải thiện hệ thống giao tiếp và tăng cường hỗ trợ từ quản lý.",
            },
          ],
        },
        {
          id: 12,
          title: "Khảo Sát Sự Hài Lòng Về Chế Độ Phúc Lợi",
          questions: [
            {
              id: 1,
              question:
                "Bạn cảm thấy chế độ phúc lợi hiện tại của công ty như thế nào?",
              type: "multiple-choice",
              options: [
                "Rất hài lòng",
                "Hài lòng",
                "Trung lập",
                "Không hài lòng",
                "Rất không hài lòng",
              ],
            },
            {
              id: 2,
              question:
                "Chế độ bảo hiểm y tế và các phúc lợi khác có đáp ứng đủ nhu cầu của bạn không?",
              type: "multiple-choice",
              options: [
                "Rất đáp ứng",
                "Đáp ứng",
                "Trung bình",
                "Không đáp ứng",
                "Rất không đáp ứng",
              ],
            },
            {
              id: 3,
              question:
                "Bạn có cảm thấy rằng chế độ nghỉ phép và thời gian làm việc là hợp lý không?",
              type: "multiple-choice",
              options: [
                "Rất hợp lý",
                "Hợp lý",
                "Trung bình",
                "Không hợp lý",
                "Rất không hợp lý",
              ],
            },
            {
              id: 4,
              question:
                "Bạn có gặp phải vấn đề gì liên quan đến việc sử dụng các phúc lợi không?",
              type: "yes-no",
            },
            {
              id: 4.1,
              question: "Nếu có, vui lòng mô tả vấn đề:",
              type: "text",
              conditional: {
                questionId: 4,
                value: "Có",
              },
            },
            {
              id: 5,
              question: "Bạn có đề xuất gì để cải thiện chế độ phúc lợi không?",
              type: "text",
            },
          ],
          responses: [
            {
              questionId: 1,
              selectedOptions: ["Hài lòng"],
            },
            {
              questionId: 2,
              selectedOptions: ["Đáp ứng"],
            },
            {
              questionId: 3,
              selectedOptions: ["Hợp lý"],
            },
            {
              questionId: 4,
              answer: "Có",
              responseDetail:
                "Có vấn đề trong việc giải quyết yêu cầu nghỉ phép.",
            },
            {
              questionId: 5,
              answer:
                "Cần cải thiện quy trình giải quyết yêu cầu phúc lợi và nâng cao chất lượng bảo hiểm y tế.",
            },
          ],
        },
        {
          id: 13,
          title: "Khảo Sát Hài Lòng Với Các Chính Sách Hỗ Trợ Công Nhân",
          questions: [
              {
                  id: 1,
                  question: "Bạn cảm thấy các chính sách hỗ trợ công nhân hiện tại của công ty như thế nào?",
                  type: "multiple-choice",
                  options: [
                      "Rất hài lòng",
                      "Hài lòng",
                      "Trung lập",
                      "Không hài lòng",
                      "Rất không hài lòng",
                  ],
              },
              {
                  id: 2,
                  question: "Bạn có cảm thấy rằng các chính sách hỗ trợ công nhân được công ty áp dụng đầy đủ không?",
                  type: "multiple-choice",
                  options: [
                      "Rất đầy đủ",
                      "Đầy đủ",
                      "Trung bình",
                      "Thiếu",
                      "Rất thiếu",
                  ],
              },
              {
                  id: 3,
                  question: "Bạn có gặp khó khăn gì trong việc tiếp cận hoặc sử dụng các chính sách hỗ trợ không?",
                  type: "yes-no",
              },
              {
                  id: 3.1,
                  question: "Nếu có, vui lòng mô tả vấn đề:",
                  type: "text",
                  conditional: {
                      questionId: 3,
                      value: "Có",
                  },
              },
              {
                  id: 4,
                  question: "Bạn có đề xuất gì để cải thiện các chính sách hỗ trợ công nhân không?",
                  type: "text",
              },
          ],
          responses: [
              {
                  questionId: 1,
                  selectedOptions: ["Hài lòng"],
              },
              {
                  questionId: 2,
                  selectedOptions: ["Đầy đủ"],
              },
              {
                  questionId: 3,
                  answer: "Có",
                  responseDetail: "Có khó khăn trong việc tiếp cận thông tin về các chính sách hỗ trợ.",
              },
              {
                  questionId: 4,
                  answer: "Cần cải thiện việc truyền thông và cung cấp thông tin rõ ràng về các chính sách hỗ trợ.",
              },
          ],
      },
      ],
      currentPage: 1,
      selectedSurvey: null,
    });

    onWillStart(() => {
      this.toggleSurvey = this.toggleSurvey.bind(this);
      this.handleSurveyClick = this.handleSurveyClick.bind(this);
      this.closeModelSurvey = this.closeModelSurvey.bind(this);
    });
  }

  toggleSurvey() {
    this.state.showSurvey = !this.state.showSurvey;
  }
  closeModelSurvey() {
    this.state.showSurvey = false;
    this.state.selectedSurvey = null;
  }

  get paginatedSurvey() {
    const startIndex = (this.state.currentPage - 1) * this.pageSize;
    const endIndex = startIndex + this.pageSize;
    return this.state.data_survey.slice(startIndex, endIndex);
  }

  nextPageSurvey() {
    if (this.state.currentPage * this.pageSize< this.state.data_survey.length) {
      this.state.currentPage += 1;
    }
  }

  handleSurveyClick(ev, survey = null) {
    if (survey) {
      this.state.showSurvey = !this.state.showSurvey;
      this.state.selectedSurvey = survey;
      console.log(survey);
    } else {
      console.log("No survey selected or survey parameter is null.");
    }
  }
  prevPageSurvey() {
    if (this.state.currentPage > 1) {
      this.state.currentPage -= 1;
    }
  }
}

Blog.template = "owl.Blog";
