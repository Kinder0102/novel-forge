import { describe, it, expect } from 'vitest'
import { ref } from 'vue'
import { useChapterGroups } from '../composables/useChapterGroups'

describe('useChapterGroups', () => {
  it('空陣列應回傳空群組', () => {
    const { chapterGroups } = useChapterGroups(ref([]), ref([]), ref([]))
    expect(chapterGroups.value).toEqual([])
  })

  it('有章節內容時應依大綱分組', () => {
    const outlines = ref([
      { id: 1, title: '大綱一', chapter_titles: [] },
      { id: 2, title: '大綱二', chapter_titles: [] },
    ])
    const titles = ref([
      { id: 10, outline_id: 1, idx: 1, title: '第一章' },
      { id: 11, outline_id: 1, idx: 2, title: '第二章' },
      { id: 20, outline_id: 2, idx: 1, title: '第三章' },
    ])
    const chapters = ref([
      { id: 101, chapter_title_id: 10, content: '第一章內容', summary: '摘要一' },
      { id: 102, chapter_title_id: 11, content: '第二章內容', summary: '摘要二' },
      { id: 201, chapter_title_id: 20, content: '第三章內容', summary: '摘要三' },
    ])

    const { chapterGroups } = useChapterGroups(outlines, chapters, titles)
    expect(chapterGroups.value).toHaveLength(2)

    
    const g1 = chapterGroups.value.find((g) => g.outlineId === 1)
    expect(g1).toBeDefined()
    expect(g1!.outlineTitle).toBe('大綱一')
    expect(g1!.chapters).toHaveLength(2)
    expect(g1!.chapters[0].title).toBe('第一章')
    expect(g1!.chapters[1].title).toBe('第二章')

    
    const g2 = chapterGroups.value.find((g) => g.outlineId === 2)
    expect(g2).toBeDefined()
    expect(g2!.outlineTitle).toBe('大綱二')
    expect(g2!.chapters).toHaveLength(1)
    expect(g2!.chapters[0].title).toBe('第三章')
  })

  it('無內容的章節應被過濾', () => {
    const outlines = ref([{ id: 1, title: '大綱一', chapter_titles: [] }])
    const titles = ref([{ id: 10, outline_id: 1, idx: 1, title: '空章節' }])
    const chapters = ref([{ id: 101, chapter_title_id: 10, content: '', summary: '' }])

    const { chapterGroups } = useChapterGroups(outlines, chapters, titles)
    expect(chapterGroups.value).toHaveLength(0)
  })

  it('無 title 的大綱應使用後備名稱', () => {
    const outlines = ref([{ id: 99, title: undefined, chapter_titles: [] }])
    const titles = ref([{ id: 10, outline_id: 99, idx: 1, title: '某章' }])
    const chapters = ref([{ id: 101, chapter_title_id: 10, content: '有內容', summary: '' }])

    const { chapterGroups } = useChapterGroups(outlines, chapters, titles)
    expect(chapterGroups.value).toHaveLength(1)
    expect(chapterGroups.value[0].outlineTitle).toBe('大綱 #99')
  })

  it('chapter_titles 中找不到對應章節時應跳過', () => {
    const outlines = ref([{ id: 1, title: '大綱一', chapter_titles: [] }])
    const titles = ref([{ id: 10, outline_id: 1, idx: 1, title: '章節A' }])
    
    const chapters = ref([{ id: 101, chapter_title_id: 999, content: '孤兒內容', summary: '' }])

    const { chapterGroups } = useChapterGroups(outlines, chapters, titles)
    expect(chapterGroups.value).toHaveLength(0)
  })

  it('群組內章節應依 idx 排序', () => {
    const outlines = ref([{ id: 1, title: '大綱一', chapter_titles: [] }])
    const titles = ref([
      { id: 12, outline_id: 1, idx: 2, title: '第二節' },
      { id: 11, outline_id: 1, idx: 1, title: '第一節' },
    ])
    const chapters = ref([
      { id: 102, chapter_title_id: 12, content: 'B', summary: '' },
      { id: 101, chapter_title_id: 11, content: 'A', summary: '' },
    ])

    const { chapterGroups } = useChapterGroups(outlines, chapters, titles)
    expect(chapterGroups.value[0].chapters[0].title).toBe('第一節')
    expect(chapterGroups.value[0].chapters[1].title).toBe('第二節')
  })

  it('重複的 chapter_title_id 應去重', () => {
    const outlines = ref([{ id: 1, title: '大綱一', chapter_titles: [] }])
    const titles = ref([{ id: 10, outline_id: 1, idx: 1, title: '重複章' }])
    const chapters = ref([
      { id: 101, chapter_title_id: 10, content: '版本一', description: '', summary: '' },
      { id: 102, chapter_title_id: 10, content: '版本二', description: '', summary: '' },
    ])

    const { chapterGroups } = useChapterGroups(outlines, chapters, titles)
    expect(chapterGroups.value[0].chapters).toHaveLength(1)
  })
})
