import { Type } from "class-transformer";
import { ArrayMaxSize, ArrayMinSize, ValidateNested } from "class-validator";

import { MAX_RESOURCE_LINKS } from "../resources.types";
import { ResourceLinkInput } from "./resource-link-input.dto";

export class AddResourceLinksDto {
  @ArrayMinSize(1)
  @ArrayMaxSize(MAX_RESOURCE_LINKS, { message: `A resource can have at most ${MAX_RESOURCE_LINKS} links` })
  @ValidateNested({ each: true })
  @Type(() => ResourceLinkInput)
  links!: ResourceLinkInput[];
}
