<script>
	import { Button, RoundButton, Tag } from '$lib/button';
	import { Note } from '$lib/info';
	import { IG, Input } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	let error = $state({});
	let filter = $state('');
	let tags = $state([]);
	let all = $derived.by(() => {
		let _temp = app.item_all_tags.filter((x) => !tags.includes(x));
		if (filter) {
			_temp = _temp.filter((x) => x.toLowerCase().includes(filter.toLowerCase()));
		}
		return _temp;
	});

	const validate = () => {
		error = {};

		if (!tags.length) {
			error.tags = 'Select the tags to delete';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Deleting Tags . . .');
		let result = await fetch(`${import.meta.env.VITE_BACKEND}/items/tag/delete`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ tags })
		});
		result = await result.json();
		loading.close();

		if (result.status == 200) {
			app.item_all_tags = result.all;
			app.item_featured_tags = result.featured;
			module.close();
			notify.open('Tags Deleted');
		} else {
			error = result;
		}
	};
</script>

<Form title="Edit Tags" error={error.error}>
	{#if tags.length}
		<IG name="To Delete" error={error.tags}>
			{#snippet input()}
				<div class="tags top">
					{#each tags as x (x)}
						<div class="tag" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
							<Tag
								onclick={() => {
									tags = tags.filter((y) => x != y);
									error = {};
								}}
							>
								{x}
							</Tag>
						</div>
					{/each}
				</div>
			{/snippet}
		</IG>
	{:else}
		<Note status={error.tags ? 400 : null} note="Select the tags to delete"></Note>
	{/if}

	<IG name="All">
		{#snippet input()}
			<div class="block">
				<div class="search">
					<Input placeholder="filter" bind:value={filter}>
						{#snippet right()}
							{#if filter}
								<div class="clear">
									<RoundButton
										--button-background-color-hover="red"
										icon="x"
										onclick={() => (filter = '')}
									></RoundButton>
								</div>
							{/if}
						{/snippet}
					</Input>
				</div>

				<div class="tags">
					{#each all as x (x)}
						<div class="tag" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
							<Tag
								onclick={() => {
									tags.push(x);
									error = {};
								}}
							>
								{x}
							</Tag>
						</div>
					{/each}
				</div>
			</div>
		{/snippet}
	</IG>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.block {
		outline: 1px solid var(--ol);
		outline-offset: -1px;
		border-radius: 4px;
		padding: 8px;
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;

		max-height: 200px;
		overflow: auto;

		&.top {
			padding: 8px;
			outline: 1px solid var(--ol);
			outline-offset: -1px;
			border-radius: 4px;
		}
	}

	.search {
		margin-bottom: 8px;
		.clear {
			margin-right: 8px;
		}
	}
</style>
