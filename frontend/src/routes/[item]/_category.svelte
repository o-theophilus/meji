<script>
	import { onMount } from 'svelte';
	import { tick, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';

	export let data;
	let { item } = data;

	let error = '';

	let all_categories = [...item.categories];
	onMount(async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}category`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				for (let i in resp.data.categories) {
					let name = resp.data.categories[i].name;
					if (!all_categories.includes(name)) {
						all_categories.push(name);
					}
				}
				all_categories = all_categories;
			} else {
				error = resp.message;
			}
		}
	});

	const submit = async () => {
		error = '';
		item.categories = clean_up();

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}category/${item.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(item)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.item);
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};

	let in_category = item.categories.join(', ');

	const clean_up = () => {
		let temp = in_category.split(',');
		let cate_list = [];
		for (let i in temp) {
			temp[i] = temp[i].trim().toLowerCase();
			if (temp[i] && !cate_list.includes(temp[i])) {
				cate_list.push(temp[i]);
			}
		}
		return cate_list;
	};
	const add_category = (cate) => {
		let cate_list = clean_up();

		cate = cate.trim().toLowerCase();
		if (cate && !cate_list.includes(cate)) {
			cate_list.push(cate);
		}

		in_category = cate_list.join(', ');
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Edit Item Categories</div>
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="category"> Categories: </label>
			<textarea type="text" bind:value={in_category} id="category" placeholder="Category here" />
			<div class="inputGroup horizontal">
				<Button
					class="tiny"
					name="Clean"
					on:click={() => {
						add_category('');
					}}
				/>
			</div>
		</div>

		<div class="inputGroup category">
			{#each all_categories as category}
				<Button
					name={category}
					class="tiny"
					on:click={() => {
						add_category(category);
					}}
				/>
			{/each}
		</div>
		{#if error}
			<p class="error">
				{error}
			</p>
		{/if}

		<div class="inputGroup horizontal">
			<Button
				class="primary"
				name="Submit"
				on:click={() => {
					submit();
				}}
			/>
		</div>
	</form>
</Form>
