<script>
	import { Icon } from '$lib/macro';

	let { children } = $props();
</script>

<div class="toc">
	<div class="title">
		<Icon icon="notebook-text"></Icon>
		Table of content
	</div>
	<div class="list">
		{@render children()}
	</div>
</div>

<style>
	.toc {
		font-size: 0.8rem;
		position: sticky;
		top: 24px;
		@media screen and (min-width: 800px) {
			top: calc(var(--headerHeight) + 24px);
		}
		height: fit-content;
		border-radius: 8px;
		overflow: hidden;

		background-color: var(--bg3);

		.title {
			display: flex;
			align-items: center;
			gap: 16px;
			font-weight: 800;
			color: var(--ft1);
			background-color: var(--bg2);
			padding: 16px 24px;
		}

		.list {
			border-top: 1px solid var(--ol);
			padding: 12px 24px;

			/* height: 200px; */
			/* overflow-y: auto; */
		}
	}
</style>
