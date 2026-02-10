<script>
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import Delete from './delete.svelte';

	let item = {
		key: module.value.key,
		status: module.value.status,
		files: module.value.files
	};
	let _status = item.status;

	let error = $state({});

	const validate = (status) => {
		error = {};

		if (status == 'active' && !item.files.length) {
			error.error = 'no photo';
		}

		Object.keys(error).length === 0 && submit(status);
	};

	const submit = async (status) => {
		loading.open('Saving Item . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ status })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.item);
			module.close();
			notify.open('Status Changed');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Change Status" error={error.error}>
	Status: <span class="status {_status}">{_status}</span>

	<br />
	<br />

	<div class="label">Change to:</div>

	{#if error.status}
		<div class="error" transition:slide>
			{error.status}
		</div>
	{/if}

	<div class="line">
		{#if _status != 'active'}
			<Button icon="check" onclick={() => validate('active')}>
				{'active'}
			</Button>
		{/if}

		{#if _status != 'draft'}
			<Button icon="square-pen" onclick={() => validate('draft')}>
				{'draft'}
			</Button>
		{/if}

		<Button
			--button-background-color-hover="red"
			icon="trash-2"
			onclick={() => module.open(Delete, { ...module.value })}
		>
			Delete
		</Button>
	</div>
</Form>

<style>
	.status {
		font-weight: 800;
	}
	.status.active {
		color: green;
	}
	.status.draft {
		color: red;
	}

	.label,
	.error {
		font-size: 0.8rem;
	}
	.error {
		color: red;
	}

	.line {
		margin-top: 8px;
	}
</style>
