document.addEventListener('DOMContentLoaded', () => {
    const formset = document.getElementById('link-formset');
    const addBtn = document.getElementById('add-link');
    if (!formset || !addBtn) return;

    const totalForms = document.getElementById('id_links-TOTAL_FORMS');

    function bindPresetHandlers(row) {
        const preset = row.querySelector('.link-preset');
        const label = row.querySelector('.link-label');
        if (!preset || !label) return;
        preset.addEventListener('change', () => {
            if (preset.value && preset.value !== 'Custom') {
                label.value = preset.value;
            }
        });
    }

    function bindDeleteHandler(row) {
        const deleteBtn = row.querySelector('.delete-link-btn');
        const deleteInput = row.querySelector('input[name$="-DELETE"]');
        if (!deleteBtn || !deleteInput) return;

        deleteBtn.addEventListener('click', () => {
            deleteInput.checked = true;
            row.classList.add('opacity-50');
            deleteBtn.disabled = true;
        });
    }

    function bindRowHandlers(row) {
        bindPresetHandlers(row);
        bindDeleteHandler(row);
    }

    formset.querySelectorAll('.link-form-row').forEach(bindRowHandlers);

    addBtn.addEventListener('click', () => {
        const count = parseInt(totalForms.value, 10);
        const template = formset.querySelector('.link-form-row');
        if (!template) return;
        const clone = template.cloneNode(true);
        clone.classList.remove('opacity-50', 'border-danger');
        clone.querySelectorAll('input, select, button').forEach((el) => {
            el.disabled = false;
        });
        clone.querySelectorAll('.text-danger').forEach((el) => el.remove());
        clone.querySelectorAll('input, select').forEach((el) => {
            if (el.name) {
                el.name = el.name.replace(/-\d+-/, `-${count}-`);
                el.id = el.id.replace(/-\d+-/, `-${count}-`);
            }
            if (el.type === 'checkbox') {
                el.checked = false;
            } else if (el.tagName === 'SELECT') {
                el.selectedIndex = 0;
            } else if (el.type !== 'hidden') {
                el.value = '';
            }
        });
        formset.appendChild(clone);
        totalForms.value = count + 1;
        bindRowHandlers(clone);
    });
});
