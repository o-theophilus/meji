<script>
	import Button from '$lib/button.svelte';
	import Card from '$lib/card.svelte';
	import Center from '$lib/Center.svelte';

	let permission = {
		admin: {
			lv1: ['dashboard'],
			lv2: ['manage_photo'],
			lv3: []
		},
		user: {
			lv1: ['view', 'view_all'],
			lv2: [],
			lv3: ['set permission']
		},
		item: {
			lv1: [],
			lv2: ['add', 'edit', 'advert', 'change_status'],
			lv3: []
		},
		voucher: {
			lv1: ['view', 'view_all'],
			lv2: [],
			lv3: ['add', 'view_code']
		},
		log: {
			lv1: ['view'],
			lv2: [],
			lv3: []
		}
	};
	let role = [];
	$: console.log(role);
</script>

<Center>
	<br />
	<div class="ctitle">Permission</div>
</Center>
<Card>
	<section>
		<span>category</span>

		{#each ['level 1', 'level 2', 'level 3'] as level}
			<span>
				<!-- <input
					type="checkbox"
					on:change={(e) => {
						console.log(e.target.checked);
					}}
				/> -->
				{level}
			</span>
		{/each}

		{#each Object.entries(permission) as [entity, levels]}
			<span>
				{entity}
			</span>
			{#each Object.entries(levels) as [_, level]}
				<span>
					{#each level as l}
						<input bind:group={role} value="{entity}:{l}" type="checkbox" />
						{l}
						<br />
					{/each}
				</span>
			{/each}
		{/each}
	</section>

	<br />
	<Button class="primary">Submit</Button>
</Card>

<style>
	section {
		display: grid;
		grid-template-columns: repeat(4, auto);
		font-size: small;
	}

	span {
		outline: 1px solid var(--ac4);
		padding: var(--sp1);
	}
</style>
