<script>
	import { module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';

	import Photo from './_photo.svelte';

	export let data;
	let { item } = data;

	let inputImg;
	let image_file;

	let src = '/image/item.png';
	let error = '';

	const on_change = () => {
		error = '';
		image_file = inputImg.files[0];
		inputImg.value = null;

		let name = image_file.name.split('.');
		let ext = name[name.length - 1];

		if (!['jpg', 'png', 'gif'].includes(ext.toLowerCase())) {
			src = '/image/item.png';
			error = 'invalid file type';
		} else {
			let reader = new FileReader();
			reader.readAsDataURL(image_file);
			reader.onload = (e) => {
				src = e.target.result;
			};
		}
	};

	const validate = () => {
		if (!image_file) {
			error = 'please select an image';
		}
		!error && submit();
	};

	const submit = async () => {
		let formData = new FormData();
		formData.append('file', image_file);
		formData.append('id', item.id);

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}photo_item/${item.key}`, {
			method: 'POST',
			headers: {
				Authorization: $token
			},
			body: formData
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.item);
				$module = {
					module: Photo,
					data: {
						item: resp.data.item
					}
				};
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Add Photo</div>
	</svelte:fragment>

	<svelte:fragment slot="info">
		<p>Select photo</p>
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<img
			{src}
			alt={item.name}
			on:click={() => {
				inputImg.click();
			}}
		/>

		{#if error}
			<div class="inputGroup">
				<p class="error">
					{error}
				</p>
			</div>
		{/if}

		<div class="inputGroup horizontal">
			<input
				type="file"
				accept=".jpg, .jpeg, .png"
				bind:this={inputImg}
				on:change={on_change}
				id="img_input"
			/>
			<Button class="primary" name="Upload" on:click={validate} />
			<Button
				name="Back"
				on:click={() => {
					$module = {
						module: Photo,
						data: {
							item
						}
					};
				}}
			/>
		</div>
	</form>
</Form>

<style>
	img {
		width: 100%;

		border-radius: var(--brad1);

		cursor: pointer;
	}

	#img_input {
		display: none;
	}
</style>
