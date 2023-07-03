<script context="module">
	import { loading } from '$lib/store.js';

	export async function load({ fetch, params, session }) {
		if (session.user.roles.includes('admin')) {
			const _resp = await fetch(`${import.meta.env.VITE_BACKEND}item/${params.item}`, {
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: session.token
				}
			});

			if (_resp.ok) {
				let resp = await _resp.json();

				if (resp.status == 200) {
					return {
						props: {
							item: resp.data.item,
							ads: resp.data.ads
						}
					};
				} else {
					return {
						status: 404,
						error: resp.message
					};
				}
			}
		}
		return {
			status: 404,
			error: 'Unauthorised Access'
		};
	}
</script>

<script>
	import { goto } from '$app/navigation';
	import { token } from '$lib/cookie.js';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';

	export let item;
	export let ads;
	let hasAds = false;
	let error = {};
	let default_src = {
		'300x300': '/image/ads_300x300.png',
		'300x600': '/image/ads_300x600.png',
		'600x300': '/image/ads_600x300.png',
		'900x300': '/image/ads_900x300.png'
	};

	let src = default_src;
	if (Object.keys(ads).length != 0) {
		hasAds = true;
		src = ads;
	}

	let input_300x300;
	let input_300x600;
	let input_600x300;
	let input_900x300;

	let image_file = {
		'300x300': '',
		'300x600': '',
		'600x300': '',
		'900x300': ''
	};

	const on_change = (e, size) => {
		error[size] = '';
		image_file[size] = '';
		image_file[size] = e.target.files[0];
		e.target.value = null;

		let name = image_file[size].name.split('.');
		let ext = name[name.length - 1];

		if (!['jpg', 'png', 'gif'].includes(ext.toLowerCase())) {
			src[size] = `/image/ads_${size}.png`;
			error[size] = 'invalid file type';
		} else {
			let reader = new FileReader();
			reader.readAsDataURL(image_file[size]);
			reader.onload = (e) => {
				let image = new Image();
				image.src = e.target.result;
				image.onload = function () {
					let dim = size.split('x');
					if (this.width != dim[0] || this.height != dim[1]) {
						error[size] = 'invalid inage size';
						image_file[size] = '';
						src[size] = `/image/ads_${size}.png`;
					} else {
						src[size] = e.target.result;
					}
				};
			};
		}
	};

	const validate = () => {
		error = {};
		if (!image_file['300x300']) {
			error['300x300'] = 'this field is required';
		}
		if (!image_file['300x600']) {
			error['300x600'] = 'this field is required';
		}
		if (!image_file['600x300']) {
			error['600x300'] = 'this field is required';
		}
		if (!image_file['900x300']) {
			error['900x300'] = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;

		let formData = new FormData();
		formData.append('300x300', image_file['300x300']);
		formData.append('300x600', image_file['300x600']);
		formData.append('600x300', image_file['600x300']);
		formData.append('900x300', image_file['900x300']);
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}photo_ads/${item.key}`, {
			method: 'post',
			headers: {
				Authorization: $token
			},
			body: formData
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				goto(`/${item.alias}`);
			} else if (resp.status == 201) {
				error = resp.message;
			} else {
				error.main = resp.message;
			}
		}
	};

	const remove_ads = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}photo_ads/${item.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				src = default_src;
				hasAds = false;
			} else if (resp.status == 201) {
				error = resp.message;
			} else {
				error.main = resp.message;
			}
		}
	};
</script>

<svelte:head>
	<title>Manage Item Ads | Meji</title>
</svelte:head>

<Card>
	<Title title="Ads" />
	<Body>
		<div class="unit">
			300x300
			<input
				type="file"
				accept=".jpg, .jpeg, .png"
				bind:this={input_300x300}
				on:change={(e) => {
					on_change(e, '300x300');
				}}
			/>

			<img
				class="_30"
				src={src['300x300']}
				alt={item.name}
				on:click={() => {
					input_300x300.click();
				}}
			/>
			{#if error['300x300']}
				<p class="error">
					{error['300x300']}
				</p>
			{/if}
		</div>

		<div class="unit">
			300x600
			<input
				type="file"
				accept=".jpg, .jpeg, .png"
				bind:this={input_300x600}
				on:change={(e) => {
					on_change(e, '300x600');
				}}
			/>

			<img
				class="_30"
				src={src['300x600']}
				alt={item.name}
				on:click={() => {
					input_300x600.click();
				}}
			/>
			{#if error['300x600']}
				<p class="error">
					{error['300x600']}
				</p>
			{/if}
		</div>

		<div class="unit">
			600x300
			<input
				type="file"
				accept=".jpg, .jpeg, .png"
				bind:this={input_600x300}
				on:change={(e) => {
					on_change(e, '600x300');
				}}
			/>

			<img
				class="_60"
				src={src['600x300']}
				alt={item.name}
				on:click={() => {
					input_600x300.click();
				}}
			/>
			{#if error['600x300']}
				<p class="error">
					{error['600x300']}
				</p>
			{/if}
		</div>

		<div class="unit">
			900x300
			<input
				type="file"
				accept=".jpg, .jpeg, .png"
				bind:this={input_900x300}
				on:change={(e) => {
					on_change(e, '900x300');
				}}
			/>

			<img
				class="_90"
				src={src['900x300']}
				alt={item.name}
				on:click={() => {
					input_900x300.click();
				}}
			/>
			{#if error['900x300']}
				<p class="error">
					{error['900x300']}
				</p>
			{/if}
		</div>

		{#if error.main}
			<p class="error">
				{error.main}
			</p>
		{/if}
		{#if !hasAds}
			<Button class="primary" name="Submit" on:click={validate} />
		{:else}
			<Button name="Remove Ads" on:click={remove_ads} />
		{/if}
	</Body>
</Card>

<style>
	.unit {
		display: grid;
		gap: var(--gap2);
		margin-bottom: var(--gap3);

		cursor: pointer;
	}
	img {
		border-radius: var(--brad1);
		height: fit-content;
	}
	._30 {
		width: 30%;
	}
	._60 {
		width: 60%;
	}
	._90 {
		width: 90%;
	}

	input {
		display: none;
	}
</style>
