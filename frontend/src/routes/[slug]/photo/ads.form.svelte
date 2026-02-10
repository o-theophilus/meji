<script>
	import { Button } from '$lib/button';
	import { Checkbox } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';

	let item = $state(module.value);
	let advert = $state(null);
	let spaces = $state([]);
	let sizes = $state([]);
	let photo_selected = $state({});
	let spaces_selected = $state([]);
	let error = $state({});
	let active = $state(null);

	let input;
	let dragover = $state(false);

	const set_active = (sz = null) => {
		if (Object.keys(photo_selected).length === 0) {
			active = null;
		} else if (sz) {
			active = sz;
		} else {
			for (const x of sizes) {
				if (photo_selected[x]) {
					active = x;
					break;
				}
				active = null;
			}
		}
	};

	const get_dimension = (file) => {
		return new Promise((resolve, reject) => {
			var reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onload = function (e) {
				var image = new Image();
				image.src = e.target.result;
				image.onload = function () {
					resolve(`${this.width}x${this.height}`);
				};
			};
		});
	};

	const on_input = async () => {
		error = {};

		let files = [];
		let picked_dimension = [];

		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];
			let dim = await get_dimension(file);
			let err = '';

			if (!['image/jpeg', 'image/png'].includes(file.type)) {
				err = `${file.name} => invalid file`;
			} else {
				if (!sizes.includes(dim)) {
					err = `${file.name} => invalid dimension`;
				} else if (advert && advert.photo[dim]) {
					err = `${file.name} => slot occupied`;
				} else if (picked_dimension.includes(dim)) {
					err = `${file.name} => slot picked`;
				}
			}

			if (err) {
				error.error = error.error ? `${error.error} <br/> ${err}` : err;
			} else {
				picked_dimension.push(dim);
				files.push(file);
			}
		}

		files.length > 0 && upload(files);
		input.value = '';
	};

	const upload = async (files) => {
		let formData = new FormData();
		for (let i in files) {
			formData.append('files', files[i]);
		}

		loading.open('uploading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${item.key}`, {
			method: 'post',
			headers: {
				Authorization: app.token
			},
			body: formData
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			advert = resp.advert;
			photo_selected = { ...advert.photo };
			spaces_selected = [...advert.space];
			if (resp.error) {
				error.error = resp.error;
			}
			set_active();
			notify.open('Ads Photo added');
			page_state.clear('adverts');
		} else {
			error = resp;
		}
	};

	const save = async () => {
		loading.open('Saving . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({
				photo_selected: Object.keys(photo_selected),
				spaces_selected
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			advert = resp.advert;
			photo_selected = { ...advert.photo };
			spaces_selected = [...advert.space];
			if (resp.error) {
				error.error = resp.error;
			}
			set_active();
			notify.open('Ads Photo added');
			page_state.clear('adverts');
		} else {
			error = resp;
		}
	};

	onMount(async () => {
		loading.open('uploading . . .');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert/${item.key}`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();

		if (resp.status == 200) {
			advert = resp.advert;
			if (advert) {
				photo_selected = { ...advert.photo };
				spaces_selected = [...advert.space];
			} else {
				advert = null;
				spaces_selected = [];
			}
			spaces = resp.spaces;
			sizes = resp.sizes;
			set_active();
		}
		loading.close();
	});
</script>

<Form title="Manage Ads Photo" error={error.error}>
	<img
		src={photo_selected[active] || '/no_photo.png'}
		alt={item.name}
		class="main"
		class:dragover
		onclick={() => {
			input.click();
		}}
		ondragover={(e) => {
			e.preventDefault();
			dragover = true;
		}}
		ondragleave={(e) => {
			e.preventDefault();
			dragover = false;
		}}
		ondrop={(e) => {
			dragover = false;

			e.preventDefault();
			input.files = e.dataTransfer.files;
			on_input();
		}}
		onerror={(e) => (e.target.src = '/no_photo.png')}
		role="presentation"
	/>
	<input
		style:display="none"
		type="file"
		accept="image/jpeg, image/png"
		multiple
		bind:this={input}
		onchange={on_input}
	/>

	<div class="carousel">
		{#each sizes as x}
			<div class="one">
				{x}
				{#if photo_selected[x]}
					<img
						class="small"
						class:active={x == active}
						src={photo_selected[x]}
						alt={item.name}
						onclick={() => {
							set_active(x);
						}}
						onerror={(e) => (e.target.src = '/no_photo.png')}
						role="presentation"
					/>
				{:else}
					<img src="/no_photo.png" alt={item.name} />
				{/if}
			</div>
		{/each}
	</div>

	<div class="checkbox">
		{#each spaces as x}
			<Checkbox
				label={x}
				value={spaces_selected.includes(x)}
				onclick={() => {
					if (spaces_selected.includes(x)) {
						spaces_selected = spaces_selected.filter((i) => i != x);
					} else {
						spaces_selected.push(x);
					}
				}}
			></Checkbox>
		{/each}
	</div>

	<div class="line">
		<Button
			icon="trash-2"
			disabled={!active}
			onclick={() => {
				let temp = { ...photo_selected };
				delete temp[active];
				photo_selected = temp;
				set_active();
			}}
		>
			Remove
		</Button>
		<Button
			icon="history"
			disabled={!advert ||
				(JSON.stringify(advert.photo) == JSON.stringify(photo_selected) &&
					JSON.stringify(advert.space) == JSON.stringify(spaces_selected))}
			onclick={() => {
				photo_selected = { ...advert.photo };
				spaces_selected = [...advert.space];
				set_active();
			}}
		>
			Reset
		</Button>
		<Button
			icon="save"
			disabled={!advert ||
				(JSON.stringify(advert.photo) == JSON.stringify(photo_selected) &&
					JSON.stringify(advert.space) == JSON.stringify(spaces_selected))}
			onclick={save}
		>
			Save
		</Button>
	</div>
</Form>

<style>
	img {
		display: block;
		width: 100%;
		background-color: var(--bg3);
		border-radius: 4px;

		&.main,
		&.small {
			outline: 2px solid transparent;
			cursor: pointer;

			transition: outline-color 0.2s ease-in-out;

			&.dragover,
			&.active,
			&:hover {
				outline-color: var(--cl1);
			}
		}
	}

	.main {
		object-fit: contain;
		aspect-ratio: 1;
	}

	.carousel {
		margin-top: 8px;
		display: flex;
		gap: 8px;

		& .one {
			display: flex;
			width: 100%;

			flex-direction: column;
			align-items: center;
			gap: 4px;
			font-size: 0.8rem;

			& img {
				&:hover {
					width: 100%;
					outline-color: var(--cl1);
				}
			}
		}
	}

	.checkbox {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
		gap: 8px 16px;

		margin: 24px 0;
	}
</style>
