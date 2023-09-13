<script>
	import { loading, portal, user, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';

	export let edit_mode = false;
	let error = {};
	let input;
	let dragover = false;
	const validate = () => {
		error = {};
		let file = input.files[0];

		let [media, type] = file.type.split('/');
		if (media != 'image' || ['svg+xml', 'x-icon'].includes(type)) {
			error.error = 'invalid file';
		}

		Object.keys(error).length === 0 && submit(file);
	};

	const submit = async (file) => {
		let formData = new FormData();
		formData.append('file', file);

		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user_photo`, {
			method: 'post',
			headers: {
				Authorization: $token
			},
			body: formData
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user = resp.user;
			$toast = {
				status: 200,
				message: 'Photo added'
			};

			error.error = resp.error;
		} else {
			error = resp;
		}
	};

	const remove = async () => {
		error = {};

		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user_photo`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user.photo = '';
			$toast = {
				status: 200,
				message: 'Photo removed'
			};
		} else {
			error = resp;
		}
	};
</script>

<img
	src={$user.photo || '/image/user.png'}
	alt={$user.name}
	onerror="this.src='/image/user.png'"
	class:dragover
	class:edit_mode
	on:click={() => {
		if (edit_mode) {
			input.click();
		}
	}}
	on:dragover|preventDefault={() => {
		dragover = true;
	}}
	on:dragenter
	on:dragleave|preventDefault={() => {
		dragover = false;
	}}
	on:drop={(e) => {
		dragover = false;
		if (edit_mode) {
			e.preventDefault();
			input.files = e.dataTransfer.files;
			validate();
		}
	}}
	role="presentation"
/>
<input
	style:display="none"
	type="file"
	accept="image/*"
	bind:this={input}
	on:change={(e) => {
		validate();
	}}
/>

<br />

{#if edit_mode}
	{#if error.error}
		<br />
		<span class="error">
			{@html error.error}
		</span>
		<br />
	{/if}

	<br />
	{#if !$user.photo}
		<Button
			class="primary small"
			on:click={() => {
				input.click();
			}}
		>
			Add
		</Button>
	{:else}
		<Button
			class="small"
			on:click={() => {
				remove('delete');
			}}
		>
			Remove
		</Button>
	{/if}
	<br />
{/if}

<style>
	img {
		width: 100%;
		padding: 0;
		border: 2px solid transparent;
		border-radius: var(--sp1);

		overflow: hidden;
	}
	img.edit_mode:hover,
	.dragover.edit_mode {
		border-color: var(--cl1);
		cursor: pointer;
	}

	img {
		width: 100%;
	}
</style>
