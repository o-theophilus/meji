<script>
	import { onMount } from 'svelte';
	import { tick, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';

	export let data;
	let { item } = data;

	let error = '';

	let all_tags = [...item.tags];
	onMount(async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}tag`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				for (let i in resp.data.tags) {
					let name = resp.data.tags[i].name;
					if (!all_tags.includes(name)) {
						all_tags.push(name);
					}
				}
				all_tags = all_tags;
			} else {
				error = resp.message;
			}
		}
	});

	const submit = async () => {
		error = '';
		item.tags = clean_up();

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}tag/${item.key}`, {
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

	let in_tag = item.tags.join(', ');

	const clean_up = () => {
		let temp = in_tag.split(',');
		let cate_list = [];
		for (let i in temp) {
			temp[i] = temp[i].trim().toLowerCase();
			if (temp[i] && !cate_list.includes(temp[i])) {
				cate_list.push(temp[i]);
			}
		}
		return cate_list;
	};
	const add_tag = (cate) => {
		let cate_list = clean_up();

		cate = cate.trim().toLowerCase();
		if (cate && !cate_list.includes(cate)) {
			cate_list.push(cate);
		}

		in_tag = cate_list.join(', ');
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Edit Item tags</div>
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="tag"> tags: </label>
			<textarea type="text" bind:value={in_tag} id="tag" placeholder="tag here" />
			<div class="inputGroup horizontal">
				<Button
					class="tiny"
					name="Clean"
					on:click={() => {
						add_tag('');
					}}
				/>
			</div>
		</div>

		<div class="inputGroup tag">
			{#each all_tags as tag}
				<Button
					name={tag}
					class="tiny"
					on:click={() => {
						add_tag(tag);
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
