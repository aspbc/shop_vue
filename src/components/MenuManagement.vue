<template>
  <div class="menu-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>菜单权限管理</span>
          <el-button type="primary" @click="handleAdd(null)">添加顶级菜单</el-button>
        </div>
      </template>

      <el-table
        :data="menuTree"
        row-key="id"
        border
        v-loading="loading"
        default-expand-all
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="menuName" label="菜单名称" width="200" />
        <el-table-column prop="icon" label="图标" width="80">
          <template #default="{ row }">
            <i :class="row.icon"></i>
          </template>
        </el-table-column>
        <el-table-column prop="path" label="路由/路径" />
        <el-table-column prop="authType" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.authType === 1 ? 'primary' : 'info'">
              {{ row.authType === 1 ? '菜单' : '功能/按钮' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="isShow" label="可见状态" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.isShow" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="{ row }">
            <el-button size="small" type="primary" text @click="handleAdd(row)">新增子菜单</el-button>
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const menuTree = ref([])
const loading = ref(false)

const buildTree = (data, pid = 0) => {
  const tree = []
  data.forEach(item => {
    if (item.pid === pid) {
      const children = buildTree(data, item.id)
      if (children.length > 0) {
        item.children = children
      }
      tree.push(item)
    }
  })
  return tree
}

const fetchMenus = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/system/menus/list')
    if (res.data.code === 200) {
      // Assuming flat list returned, build tree on frontend
      menuTree.value = buildTree(res.data.data, 0)
    }
  } catch (error) {
    ElMessage.error('获取菜单列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = (parent) => {
  ElMessage.info('暂未实现详细弹窗表单')
}

const handleEdit = (row) => {
  ElMessage.info('暂未实现详细弹窗表单')
}

const handleStatusChange = async (row) => {
  try {
    await axios.post('/api/admin/system/menus/save', row)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.isShow = row.isShow === 1 ? 0 : 1
    ElMessage.error('状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此菜单吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/system/menus/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchMenus()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchMenus()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
