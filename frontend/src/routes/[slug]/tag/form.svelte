<script>
	import { Button, Tag } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	let error = $state({});
	let init = module.value.tags;
	let tags_string = $state(init.join(', '));
	let tags = $derived(
		tags_string
			.replace(/\r?\n/g, ',')
			.replace(/\s+/g, ' ')
			.toLowerCase()
			.split(',')
			.map((i) => i.trim())
			.filter(Boolean)
			.filter((v, i, arr) => arr.indexOf(v) === i)
	);
	let unused_tags = $derived.by(() => {
		if (!app.item_all_tags) return [];
		return app.item_all_tags.filter((i) => !tags.includes(i));
	});

	const validate = () => {
		error = {};

		if (JSON.stringify(tags.sort()) === JSON.stringify(init.sort())) {
			error.tags = 'No changes were made';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Saving Item . . .');
		let response = await fetch(`${import.meta.env.VITE_BACKEND}/items/${module.value.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ tags })
		});
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			module.value.update(result.item);
			module.close();
			notify.open(`Tag${result.item.tags.length > 1 ? 's' : ''} Saved`);
		} else {
			error = result;
		}
	};

	const clean_value = (tag = '') => {
		tags_string += `, ${tag}`;
		tags_string = tags.join(', ');
	};

	let _loading = true;
	onMount(async () => {
		if (tags_string == '') {
			tags_string = module.value.name.split(' ').join(', ');
		}

		if (!app.item_all_tags) {
			let result = await fetch(`${import.meta.env.VITE_BACKEND}/tags`);
			result = await result.json();

			if (result.status == 200) {
				app.item_all_tags = result.tags;
			}
		}
		_loading = false;
	});
</script>

<Form title="Edit Tags" error={error.error}>
	<IG
		name="Tags"
		bind:value={tags_string}
		error={error.tags}
		type="textarea"
		placeholder="Tags here"
		onblur={() => clean_value()}
	/>

	<IG name="All">
		{#snippet input()}
			<div class="tags">
				{#each unused_tags as x (x)}
					<div
						class="tag"
						class:featured={app.item_featured_tags.includes(x)}
						animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
					>
						<Tag
							onclick={() => {
								clean_value(x);
							}}
						>
							{x}
						</Tag>
					</div>
				{/each}
			</div>
		{/snippet}
	</IG>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;

		max-height: 200px;
		padding: 8px;
		overflow: auto;

		outline: 1px solid var(--ol);
		outline-offset: -1px;
		border-radius: 4px;
	}

	.featured {
		--tag-background-color: var(--cl1);
		--button-background-color-hover: var(--cl1_);
		--tag-color: white;
		--button-color-hover: white;
		--tag-outline-color: transparent;
		--tag-outline-color-hover: transparent;
	}
</style>
